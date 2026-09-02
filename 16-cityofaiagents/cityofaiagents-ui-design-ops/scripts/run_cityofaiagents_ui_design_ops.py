#!/usr/bin/env python3
"""Build a structured UI design-operations brief for the mirrored skill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "sdlc-system" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sdlc_common import flatten_text, load_artifact, write_artifact  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Build a UI design-operations brief.")
    parser.add_argument("--input", required=True, help="Input artifact path")
    parser.add_argument("--output", default="ui_design_ops_plan.json", help="Output artifact path")
    args = parser.parse_args()

    payload = load_artifact(args.input)
    text = flatten_text(payload).lower()

    focus_areas = []
    if any(token in text for token in ("nav", "sidebar", "header", "menu")):
        focus_areas.append("navigation structure")
    if any(token in text for token in ("spacing", "grid", "alignment", "layout")):
        focus_areas.append("layout and spacing")
    if any(token in text for token in ("theme", "color", "contrast", "visual")):
        focus_areas.append("visual hierarchy and theming")
    if any(token in text for token in ("accessibility", "rtl", "keyboard", "screen reader")):
        focus_areas.append("accessibility and localization")
    if not focus_areas:
        focus_areas.append("desktop UI structure")

    report = {
        "artifact_type": "cityofaiagents-ui-design-ops-brief",
        "artifact_id": "SKL-0010",
        "revision": 3,
        "supported_tags": [
            "ui-design",
            "ux-strategy",
            "visual-design",
            "desktop-ui",
            "theme-system",
            "accessibility",
            "design-research",
        ],
        "focus_areas": focus_areas,
        "reference_urls": [
            "https://developer.apple.com/design/human-interface-guidelines/layout",
            "https://fluent2.microsoft.design/layout",
            "https://m3.material.io/",
            "https://www.nngroup.com/articles/ten-usability-heuristics/",
        ],
        "input_summary": flatten_text(payload)[:240],
    }

    path = write_artifact(report, args.output, "json")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
