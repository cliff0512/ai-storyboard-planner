import json
import tempfile
import unittest
from pathlib import Path

from prompts import SHOT_TEMPLATES
from storyboard import load_scenes, plan_shots


def sample_file() -> Path:
    data = {
        "project": "demo",
        "episode": 2,
        "scenes": [
            {"title": "A", "description": "scene a", "duration_s": 9},
            {"title": "B", "description": "scene b", "duration_s": 6},
        ],
    }
    path = Path(tempfile.mkdtemp()) / "scenes.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


class PlanShotsTest(unittest.TestCase):
    def test_every_scene_expands_to_full_coverage(self):
        _, episode, scenes = load_scenes(sample_file())
        shots = plan_shots(episode, scenes)
        self.assertEqual(len(shots), 2 * len(SHOT_TEMPLATES))
        self.assertEqual(shots[0].shot_id, "EP02_SH001")
        self.assertEqual(shots[-1].shot_id, "EP02_SH006")

    def test_duration_is_split_evenly_across_shots(self):
        _, episode, scenes = load_scenes(sample_file())
        shots = plan_shots(episode, scenes)
        self.assertTrue(all(s.duration_s == 3.0 for s in shots[:3]))
        self.assertTrue(all(s.duration_s == 2.0 for s in shots[3:]))

    def test_prompt_mentions_characters_and_mood(self):
        _, episode, scenes = load_scenes(sample_file())
        shots = plan_shots(episode, scenes)
        self.assertIn("Mood: neutral", shots[0].prompt)


if __name__ == "__main__":
    unittest.main()
