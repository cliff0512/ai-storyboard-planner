#!/usr/bin/env python3
"""ai-storyboard-planner: turn a scene list into a production shot list.

Reads a JSON file describing the scenes of an episode and expands every
scene into a standard three-shot coverage pattern (establishing / medium /
close-up). Each shot gets a stable production id (EP01_SH001 ...), a camera
note, a duration estimate and a ready-to-use image/video generation prompt.

Stdlib only. Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

from prompts import SHOT_TEMPLATES, STYLE_SUFFIX


@dataclass
class Scene:
    title: str
    description: str
    mood: str = "neutral"
    characters: list = field(default_factory=list)
    duration_s: float = 6.0


@dataclass
class Shot:
    shot_id: str
    scene_title: str
    shot_type: str
    camera: str
    duration_s: float
    prompt: str


def load_scenes(path: Path) -> tuple[str, int, list[Scene]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", "untitled")
    episode = int(data.get("episode", 1))
    scenes = [Scene(**s) for s in data["scenes"]]
    return project, episode, scenes


def build_prompt(scene: Scene, shot_type: str) -> str:
    template = SHOT_TEMPLATES[shot_type]
    who = ", ".join(scene.characters) if scene.characters else "no characters"
    return (
        f"{template['framing']}: {scene.description} "
        f"Characters: {who}. Mood: {scene.mood}. {STYLE_SUFFIX}"
    )


def plan_shots(episode: int, scenes: list[Scene]) -> list[Shot]:
    shots: list[Shot] = []
    counter = 0
    for scene in scenes:
        per_shot = round(scene.duration_s / len(SHOT_TEMPLATES), 2)
        for shot_type, template in SHOT_TEMPLATES.items():
            counter += 1
            shots.append(
                Shot(
                    shot_id=f"EP{episode:02d}_SH{counter:03d}",
                    scene_title=scene.title,
                    shot_type=shot_type,
                    camera=template["camera"],
                    duration_s=per_shot,
                    prompt=build_prompt(scene, shot_type),
                )
            )
    return shots


def to_markdown(project: str, shots: list[Shot]) -> str:
    lines = [
        f"# Shot list — {project}",
        "",
        "| Shot | Scene | Type | Camera | Duration (s) | Prompt |",
        "|---|---|---|---|---|---|",
    ]
    for s in shots:
        lines.append(
            f"| {s.shot_id} | {s.scene_title} | {s.shot_type} | {s.camera} "
            f"| {s.duration_s} | {s.prompt} |"
        )
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Expand a scene list into a production shot list."
    )
    ap.add_argument("scenes", type=Path, help="JSON file describing the episode's scenes")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the Markdown shot list here (default: stdout)",
    )
    ap.add_argument("--json", type=Path, help="Also write the shot list as JSON here")
    args = ap.parse_args(argv)

    project, episode, scenes = load_scenes(args.scenes)
    shots = plan_shots(episode, scenes)

    md = to_markdown(project, shots)
    if args.output:
        args.output.write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    if args.json:
        args.json.write_text(
            json.dumps([asdict(s) for s in shots], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
