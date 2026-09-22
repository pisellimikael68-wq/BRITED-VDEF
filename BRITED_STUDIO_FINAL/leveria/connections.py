from __future__ import annotations

import json
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SERVICE = "fr.brited.studio"
PLATFORMS = ("instagram", "tiktok", "youtube")
REQUIRED = {
    "instagram": ("app_id", "app_secret", "access_token", "instagram_user_id"),
    "tiktok": ("client_key", "client_secret", "access_token", "open_id"),
    "youtube": ("client_id", "client_secret", "refresh_token"),
}


class KeychainUnavailable(RuntimeError):
    pass


class MacOSKeychain:
    """Stocke les secrets dans le Trousseau macOS, jamais dans le dépôt."""

    def __init__(self, service: str = SERVICE):
        self.service = service

    @staticmethod
    def available() -> bool:
        return platform.system() == "Darwin"

    def _account(self, platform_id: str, key: str) -> str:
        if platform_id not in PLATFORMS or key not in REQUIRED[platform_id]:
            raise ValueError("Identifiant de secret inconnu")
        return f"{platform_id}.{key}"

    def set(self, platform_id: str, key: str, value: str) -> None:
        if not self.available():
            raise KeychainUnavailable("Le Trousseau macOS n'est pas disponible")
        value = value.strip()
        if not value:
            raise ValueError("Un secret vide ne peut pas être enregistré")
        subprocess.run(
            ["security", "add-generic-password", "-U", "-s", self.service,
             "-a", self._account(platform_id, key), "-w", value],
            check=True, capture_output=True, text=True,
        )

    def get(self, platform_id: str, key: str) -> str | None:
        if not self.available():
            return None
        result = subprocess.run(
            ["security", "find-generic-password", "-s", self.service,
             "-a", self._account(platform_id, key), "-w"],
            capture_output=True, text=True,
        )
        return result.stdout.strip() if result.returncode == 0 else None


@dataclass(frozen=True)
class ConnectionStatus:
    platform: str
    configured: bool
    missing: tuple[str, ...]
    mode: str
    next_step: str

    def json(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "configured": self.configured,
            "missing": list(self.missing),
            "mode": self.mode,
            "next_step": self.next_step,
        }


class PlatformConnections:
    """État local des API. Aucun appel externe n'est effectué à l'affichage."""

    def __init__(self, root: Path, vault: MacOSKeychain | None = None):
        self.root = root.resolve()
        self.vault = vault or MacOSKeychain()
        self.state_path = self.root / "data" / "platform_connections.json"

    def _public_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {"schema": "brited.platform-connections.v1", "platforms": {}}
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def status(self) -> dict[str, Any]:
        public = self._public_state().get("platforms", {})
        statuses = []
        for name in PLATFORMS:
            missing = tuple(key for key in REQUIRED[name] if not self.vault.get(name, key))
            configured = not missing
            statuses.append(ConnectionStatus(
                platform=name,
                configured=configured,
                missing=missing,
                mode="api_officielle" if configured else "configuration_requise",
                next_step=("Tester l'autorisation sans publier" if configured
                           else str(public.get(name, {}).get("next_step") or self.instructions(name))),
            ).json())
        return {
            "keychain": self.vault.available(),
            "all_configured": all(item["configured"] for item in statuses),
            "publication_locked": True,
            "platforms": statuses,
        }

    @staticmethod
    def instructions(name: str) -> str:
        return {
            "youtube": "Créer un client OAuth Bureau dans Google Cloud et activer YouTube Data API v3.",
            "instagram": "Créer une app Meta, activer Instagram API et relier le compte professionnel.",
            "tiktok": "Créer une app TikTok Developer, ajouter Content Posting API et demander video.upload/video.publish.",
        }[name]

    def save_public_setup(self, name: str, values: dict[str, str]) -> dict[str, Any]:
        if name not in PLATFORMS:
            raise ValueError("Plateforme inconnue")
        secret_keys = set(REQUIRED[name])
        unknown = set(values) - secret_keys
        if unknown:
            raise ValueError("Champ de connexion inconnu")
        for key, value in values.items():
            if value.strip():
                self.vault.set(name, key, value)
        state = self._public_state()
        state.setdefault("platforms", {})[name] = {
            "next_step": "Tester l'autorisation sans publier",
            "secrets_location": "Trousseau macOS",
        }
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return self.status()

