from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


DESTINATIONS = ("instagram", "tiktok", "youtube", "facebook")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def section(markdown: str, heading: str) -> str:
    match = re.search(
        rf"(?ims)^##\s+{re.escape(heading)}\s*$\s*(.*?)(?=^##\s+|\Z)",
        markdown,
    )
    return (match.group(1) if match else "").strip()


def publication_text(markdown: str) -> tuple[str, list[str]]:
    legend = section(markdown, "Légende")
    hashtags = re.findall(r"#[\wÀ-ÿ]+", section(markdown, "Hashtags"))
    return legend, hashtags


class NativeDistribution:
    """Prépare un lot vérifié pour les programmateurs natifs, sans transfert externe."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def _manifest_path(self, relative: str) -> Path:
        path = (self.root / relative).resolve()
        production = (self.root / "production").resolve()
        if production not in path.parents or path.name != "manifest.json" or not path.is_file():
            raise ValueError("Manifeste BRITED introuvable ou hors du dossier Production")
        return path

    def _validated_manifest(self, path: Path) -> dict[str, Any]:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("status") != "approved" or not manifest.get("approved_for_publication_workflow"):
            raise ValueError("Le lot doit être entièrement validé avant sa préparation")
        if manifest.get("publish_locked") is not True:
            raise ValueError("Le verrou de publication BRITED est absent")
        items = manifest.get("items") or []
        if not items or any(item.get("status") != "approved" for item in items):
            raise ValueError("Une vidéo du lot n'est pas validée")
        return manifest

    def prepare(self, manifest_relative: str) -> dict[str, Any]:
        manifest_path = self._manifest_path(manifest_relative)
        manifest = self._validated_manifest(manifest_path)
        scheduled_time = "10:00" if int(manifest.get("slot", 0)) == 1 else "17:00"
        posts: list[dict[str, Any]] = []
        alerts: list[str] = []

        for item in manifest["items"]:
            video = Path(str(item.get("video", ""))).resolve()
            script = Path(str(item.get("script", ""))).resolve()
            if not video.is_file() or not script.is_file():
                raise ValueError("Une vidéo ou son script source est absent")
            if self.root not in video.parents or self.root not in script.parents:
                raise ValueError("Une source se trouve hors de BRITED")
            actual_video_hash = sha256(video)
            if actual_video_hash != item.get("video_sha256"):
                raise ValueError("Une vidéo a changé depuis sa validation")
            if sha256(script) != item.get("script_sha256"):
                raise ValueError("Un script a changé depuis sa validation")
            trace_path = video.with_suffix(".render-trace.json")
            if not trace_path.is_file():
                raise ValueError("La preuve de cadrage propre à la plateforme est absente")
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
            features = trace.get("features", {})
            if (features.get("delivery_profile") != item.get("delivery_profile") or
                    not features.get("platform_specific_composition")):
                raise ValueError("Le rendu n'est pas certifié pour sa plateforme de destination")

            audit = item.get("audit") or {}
            if not audit.get("ok", False):
                alerts.append(
                    f"{item.get('platform')}: ancienne alerte d'audit conservée "
                    f"(validation humaine officielle prioritaire)"
                )
            markdown = script.read_text(encoding="utf-8")
            caption, hashtags = publication_text(markdown)
            destinations = item.get("distribution_destinations") or (
                ["youtube"] if item.get("platform") == "shorts" else ["instagram"]
            )
            for destination in destinations:
                if destination not in DESTINATIONS:
                    raise ValueError(f"Destination inconnue : {destination}")
                posts.append({
                    "destination": destination,
                    "title": str(item.get("title", "")).strip(),
                    "caption": caption,
                    "hashtags": hashtags,
                    "scheduled_date": manifest["date"],
                    "scheduled_time": scheduled_time,
                    "timezone": "Europe/Paris",
                    "video": str(video),
                    "video_sha256": actual_video_hash,
                    "script": str(script),
                    "script_sha256": item["script_sha256"],
                    "publication_id": item.get("publication_id", ""),
                    "delivery_profile": item.get("delivery_profile", item.get("platform", "")),
                    "state": "local_ready",
                    "uploaded": False,
                    "scheduled": False,
                    "published": False,
                    "delivery_mode": "instagram_crosspost" if destination == "facebook" else "native_api",
                })

        posts.sort(key=lambda post: DESTINATIONS.index(post["destination"]))
        if [post["destination"] for post in posts] != list(DESTINATIONS):
            raise ValueError("Le lot doit contenir exactement Instagram, TikTok, YouTube et Facebook")
        by_destination = {post["destination"]: post for post in posts}
        expected_profiles = {"instagram": "reels", "facebook": "reels",
                             "tiktok": "tiktok", "youtube": "shorts"}
        for destination, profile in expected_profiles.items():
            if by_destination[destination].get("delivery_profile") != profile:
                raise ValueError(f"Profil visuel incorrect pour {destination} : {profile} requis")
        # Facebook est le partage natif du Reel Instagram. TikTok et YouTube
        # doivent impérativement disposer de leurs propres compositions.
        if by_destination["instagram"]["video_sha256"] != by_destination["facebook"]["video_sha256"]:
            raise ValueError("Instagram et Facebook doivent partager le rendu Reels validé")
        if by_destination["youtube"]["video_sha256"] in {
            by_destination["instagram"]["video_sha256"], by_destination["tiktok"]["video_sha256"]
        } or by_destination["tiktok"]["video_sha256"] == by_destination["instagram"]["video_sha256"]:
            raise ValueError("Les rendus Reels, TikTok et YouTube doivent avoir des empreintes distinctes")

        package = {
            "schema": "brited.native-distribution.v1",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "source_manifest": str(manifest_path.relative_to(self.root)),
            "source_manifest_sha256": sha256(manifest_path),
            "date": manifest["date"],
            "slot": manifest["slot"],
            "status": "ready_for_explicit_transfer_confirmation",
            "publish_locked": True,
            "external_transfer_completed": False,
            "scheduled": False,
            "published": False,
            "alerts": alerts,
            "posts": posts,
        }
        target_dir = manifest_path.parent / "distribution"
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "native-package.json"
        target.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {**package, "path": str(target.relative_to(self.root))}
