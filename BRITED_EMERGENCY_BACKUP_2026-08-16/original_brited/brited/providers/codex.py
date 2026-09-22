"""Production HTTP provider for Codex-compatible endpoints."""

from __future__ import annotations

import json
import socket
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .errors import (
    ProviderConfigurationError,
    ProviderErrorKind,
    ProviderInvocationError,
    ProviderValidationError,
)
from .interface import Provider
from .models import ProviderDiagnostic, ProviderRequest, ProviderResponse
from .validator import (
    validate_provider_request,
    validate_provider_response,
)


@dataclass(frozen=True, slots=True)
class _HttpResponse:
    status: int
    body: bytes


class _HttpClient(Protocol):
    def post(
        self,
        endpoint: str,
        *,
        headers: Mapping[str, str],
        body: bytes,
        timeout: float,
    ) -> _HttpResponse: ...


class _UrllibHttpClient:
    def post(
        self,
        endpoint: str,
        *,
        headers: Mapping[str, str],
        body: bytes,
        timeout: float,
    ) -> _HttpResponse:
        request = Request(
            endpoint,
            data=body,
            headers=dict(headers),
            method="POST",
        )

        print("\n========== OPENAI REQUEST ==========")
        print("Endpoint :", endpoint)
        print("Headers  :")
        for key, value in headers.items():
            if key.lower() == "authorization":
                print(f"  {key}: Bearer ***")
            else:
                print(f"  {key}: {value}")
        print("Payload :")
        print(body.decode("utf-8", errors="replace"))
        print("====================================")

        try:
            with urlopen(request, timeout=timeout) as response:
                response_body = response.read()

                print("\n========== OPENAI RESPONSE ==========")
                print("HTTP :", response.status)
                print(response_body.decode("utf-8", errors="replace"))
                print("=====================================\n")

                return _HttpResponse(response.status, response_body)

        except HTTPError as error:
            response_body = error.read()

            print("\n========== OPENAI HTTP ERROR ==========")
            print("HTTP :", error.code)
            print(response_body.decode("utf-8", errors="replace"))
            print("=======================================\n")

            return _HttpResponse(error.code, response_body)

        except URLError as error:
            print("\n========== OPENAI NETWORK ERROR ==========")
            print(repr(error))
            print("==========================================\n")
            raise


class CodexProvider(Provider):
    """Invoke one configured Codex-compatible HTTP endpoint."""

    def __init__(
        self,
        *,
        endpoint: str,
        model: str,
        api_key: str,
        timeout: float,
        _http_client: _HttpClient | None = None,
    ) -> None:
        self._endpoint = self._required_text(endpoint, "endpoint")
        self._model = self._required_text(model, "model")
        self._api_key = self._required_text(api_key, "api_key")
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise ProviderConfigurationError(
                "timeout must be a positive number",
                diagnostics=(
                    ProviderDiagnostic(
                        "$.timeout",
                        "invalid_timeout",
                        "must be a positive number",
                    ),
                ),
            )
        if _http_client is not None and not callable(
            getattr(_http_client, "post", None)
        ):
            raise ProviderConfigurationError(
                "_http_client must provide post()",
                diagnostics=(
                    ProviderDiagnostic(
                        "$._http_client",
                        "invalid_http_client",
                        "must provide a callable post method",
                    ),
                ),
            )
        self._timeout = float(timeout)
        self._http_client = _http_client or _UrllibHttpClient()

    def invoke(self, request: ProviderRequest) -> ProviderResponse:
        normalized = validate_provider_request(request)
        payload = json.dumps(
            {
                "input": normalized.content,
                "metadata": {"request_id": normalized.request_id},
                "model": self._model,
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        try:
            response = self._http_client.post(
                self._endpoint,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                body=payload,
                timeout=self._timeout,
            )

            print("\n========== OPENAI ==========")
            print("Endpoint :", self._endpoint)
            print("Model    :", self._model)
            print("API key  :", "présente" if self._api_key else "absente")
            print("HTTP     :", response.status)
            print("Réponse  :")
            print(response.body.decode("utf-8", errors="replace"))
            print("============================\n")

        except (TimeoutError, socket.timeout) as error:
            raise self._invocation_error(
                "timeout",
                "Codex request timed out",
                retryable=True,
            ) from error
        except URLError as error:
            raise self._invocation_error(
                "unavailable",
                "Codex endpoint is unavailable",
                retryable=True,
            ) from error
        except Exception as error:
            raise self._invocation_error(
                "unknown_error",
                "Codex invocation failed",
                retryable=False,
            ) from error

        if response.status in {401, 403}:
            raise self._invocation_error(
                "authentication",
                "Codex authentication failed",
                retryable=False,
            )
        if response.status == 408:
            raise self._invocation_error(
                "timeout",
                "Codex request timed out",
                retryable=True,
            )
        if response.status == 429 or 500 <= response.status <= 599:
            raise self._invocation_error(
                "unavailable",
                "Codex endpoint is unavailable",
                retryable=True,
            )
        if not 200 <= response.status <= 299:
            raise self._invocation_error(
                "unknown_error",
                "Codex endpoint returned an unexpected status",
                retryable=False,
            )

        return self._response(normalized.request_id, response.body)

    @staticmethod
    def _required_text(value: object, field: str) -> str:
        if (
            not isinstance(value, str)
            or not value
            or value != value.strip()
        ):
            raise ProviderConfigurationError(
                f"{field} must be a non-empty string without whitespace",
                diagnostics=(
                    ProviderDiagnostic(
                        f"$.{field}",
                        "invalid_configuration",
                        "must be a non-empty string without whitespace",
                    ),
                ),
            )
        return value

    @staticmethod
    def _response(
        request_id: str,
        body: bytes,
    ) -> ProviderResponse:
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise CodexProvider._invalid_response(
                "response body must be valid UTF-8 JSON"
            ) from error
        if not isinstance(payload, dict):
            raise CodexProvider._invalid_response(
                "response body must be a JSON object"
            )
        content = payload.get("output_text")
        if content is None:
            content = CodexProvider._output_text(payload.get("output"))
        external_id = payload.get("id")
        if not isinstance(content, str) or not content:
            raise CodexProvider._invalid_response(
                "response output_text must be a non-empty string"
            )
        if external_id is not None and (
            not isinstance(external_id, str)
            or not external_id
            or external_id != external_id.strip()
        ):
            raise CodexProvider._invalid_response(
                "response id must be a non-empty string when present"
            )
        return validate_provider_response(
            ProviderResponse(
                request_id=request_id,
                content=content,
                provider_request_id=external_id,
            ),
            expected_request_id=request_id,
        )

    @staticmethod
    def _output_text(output: object) -> str | None:
        if not isinstance(output, list):
            return None
        texts = []
        for item in output:
            if not isinstance(item, dict) or item.get("type") != "message":
                continue
            parts = item.get("content")
            if not isinstance(parts, list):
                continue
            for part in parts:
                if (
                    isinstance(part, dict)
                    and part.get("type") == "output_text"
                    and isinstance(part.get("text"), str)
                ):
                    texts.append(part["text"])
        return "".join(texts) or None

    @staticmethod
    def _invalid_response(message: str) -> ProviderValidationError:
        return ProviderValidationError(
            ProviderErrorKind.INVALID_RESPONSE,
            [
                ProviderDiagnostic(
                    "$.response",
                    "invalid_response",
                    message,
                )
            ],
        )

    @staticmethod
    def _invocation_error(
        code: str,
        message: str,
        *,
        retryable: bool,
    ) -> ProviderInvocationError:
        return ProviderInvocationError(
            message,
            retryable=retryable,
            diagnostics=(
                ProviderDiagnostic(
                    "$.response",
                    code,
                    message,
                ),
            ),
        )
