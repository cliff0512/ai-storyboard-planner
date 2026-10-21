"""Shot templates used by storyboard.py.

Each template describes a framing and a default camera note. The scene
description is combined with the template to build a ready-to-use
image/video generation prompt for every shot.
"""

STYLE_SUFFIX = "cinematic lighting, high detail, consistent character design"

SHOT_TEMPLATES = {
    "establishing": {
        "framing": "Wide establishing shot",
        "camera": "Static wide shot, slow push-in",
    },
    "medium": {
        "framing": "Medium shot",
        "camera": "Handheld medium shot, slight pan following the action",
    },
    "close_up": {
        "framing": "Close-up shot",
        "camera": "Close-up, shallow depth of field, focus on facial expression",
    },
}
