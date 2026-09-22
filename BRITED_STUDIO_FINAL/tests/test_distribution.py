from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from leveria.distribution import NativeDistribution, sha256


class NativeDistributionTests(unittest.TestCase):
    def fixture(self, approved: bool = True):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        folder = root / "production/2026-08-24/slot-1"
        videos = {}
        for platform, content in (("reels", b"reels-video"),
                                  ("tiktok", b"tiktok-video"),
                                  ("shorts", b"youtube-video")):
            video = folder / platform / "video.mp4"
            video.parent.mkdir(parents=True, exist_ok=True)
            video.write_bytes(content)
            video.with_suffix(".render-trace.json").write_text(json.dumps({"features": {
                "delivery_profile": platform, "platform_specific_composition": True}}))
            videos[platform] = video
        scripts = root / "scripts"
        scripts.mkdir()
        youtube_script = scripts / "youtube.md"
        youtube_script.write_text("## Légende\nLégende YouTube\n\n## Hashtags\n#shorts", encoding="utf-8")
        state = "approved" if approved else "awaiting_approval"
        manifest = {
            "date": "2026-08-24", "slot": 1, "status": state,
            "publish_locked": True, "approved_for_publication_workflow": approved,
            "items": [{"publication_id": platform, "platform": platform, "title": "Titre",
                 "script": str(youtube_script), "video": str(video),
                 "script_sha256": sha256(youtube_script), "video_sha256": sha256(video),
                 "status": state, "audit": {"ok": True}, "delivery_profile": platform,
                 "distribution_destinations": {"reels": ["instagram", "facebook"],
                    "tiktok": ["tiktok"], "shorts": ["youtube"]}[platform]}
                for platform, video in videos.items()],
        }
        path = folder / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return temporary, root, path

    def test_prepares_four_locked_native_posts_without_transfer(self):
        temporary, root, path = self.fixture()
        with temporary:
            result = NativeDistribution(root).prepare(str(path.relative_to(root)))
            self.assertEqual(["instagram", "tiktok", "youtube", "facebook"], [p["destination"] for p in result["posts"]])
            self.assertEqual(3, len({p["video_sha256"] for p in result["posts"]}))
            self.assertEqual("instagram_crosspost", result["posts"][3]["delivery_mode"])
            self.assertEqual("10:00", result["posts"][0]["scheduled_time"])
            self.assertTrue(result["publish_locked"])
            self.assertFalse(result["external_transfer_completed"])
            self.assertFalse(result["scheduled"])
            self.assertFalse(result["published"])
            self.assertTrue((root / result["path"]).is_file())

    def test_refuses_unapproved_manifest(self):
        temporary, root, path = self.fixture(approved=False)
        with temporary, self.assertRaisesRegex(ValueError, "validé"):
            NativeDistribution(root).prepare(str(path.relative_to(root)))

    def test_refuses_a_video_changed_after_validation(self):
        temporary, root, path = self.fixture()
        with temporary:
            manifest = json.loads(path.read_text())
            Path(manifest["items"][0]["video"]).write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "changé"):
                NativeDistribution(root).prepare(str(path.relative_to(root)))


if __name__ == "__main__":
    unittest.main()
