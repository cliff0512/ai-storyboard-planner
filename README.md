# ai-storyboard-planner

Turn a simple scene list into a **production-ready shot list** for AI-generated
video: stable shot IDs, camera notes, duration splits, and ready-to-use
image/video generation prompts for every shot.

Built for independent creators who produce short AI-animated episodes and need
the same discipline a film crew gets from a storyboard — without the crew.

## Why

AI video tools generate one clip at a time. Without a shot list, a 2-minute
episode quickly turns into a pile of unrelated clips: characters drift, shot
sizes repeat, and nothing cuts together. This tool enforces a standard
coverage pattern (establishing → medium → close-up) with consistent
`EP01_SH001`-style IDs, so every generated clip has a planned place in the edit.

## Install

No dependencies — Python 3.9+ standard library only.

```bash
git clone https://github.com/cliff0512/ai-storyboard-planner.git
cd ai-storyboard-planner
```

## Usage

Describe the scenes of an episode in JSON (see `sample_scene.json`):

```json
{
  "project": "Robby Star — Episode 1",
  "episode": 1,
  "scenes": [
    {
      "title": "Arrival at the valley",
      "description": "A small robot scout descends into a misty green valley at dawn",
      "mood": "wonder",
      "characters": ["Luka the robot scout"],
      "duration_s": 9
    }
  ]
}
```

Generate the shot list:

```bash
python storyboard.py sample_scene.json -o shotlist.md --json shotlist.json
```

Output (excerpt):

| Shot | Scene | Type | Camera | Duration (s) | Prompt |
|---|---|---|---|---|---|
| EP01_SH001 | Arrival at the valley | establishing | Static wide shot, slow push-in | 3.0 | Wide establishing shot: A small robot scout descends into a misty green valley at dawn. Characters: Luka the robot scout. Mood: wonder. cinematic lighting, high detail, consistent character design |
| EP01_SH002 | Arrival at the valley | medium | Handheld medium shot, slight pan following the action | 3.0 | Medium shot: ... |
| EP01_SH003 | Arrival at the valley | close_up | Close-up, shallow depth of field | 3.0 | Close-up shot: ... |

Feed each prompt to your image/video generator of choice, name the clips by
shot ID, and the episode assembles in order.

## Tests

```bash
python -m unittest test_storyboard -v
```

## Roadmap

- [ ] Custom coverage patterns per scene type (dialogue, action, montage)
- [ ] Character consistency blocks injected into every prompt
- [ ] CSV export for editing software
- [ ] Optional LLM backend for automatic scene breakdown from a script

## Contributing

Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

## Maintainer

Lifeng Cao ([@cliff0512](https://github.com/cliff0512)) — creator and primary
maintainer. This project is actively maintained as part of an independent
AI-animation production workflow.
