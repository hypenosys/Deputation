#!/usr/bin/env python3
"""Validate authored color/UX content and original SVG wireframes (stdlib only).

This is NOT evidence that the Godot scene runs or that the C64 displays these
RGB colors. Full Godot headless smoke is a separate CI gate.
"""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "data/design/visual_palette.v1.json"
CONTENT = ROOT / "data/design/narrative_content.v1.json"
WIREFRAMES = ROOT / "docs/design/wireframes"
HEX = re.compile(r"#[0-9A-Fa-f]{6}\Z")
EXPECTED = {"case_open.svg", "task_list.svg", "administrative_view.svg"}
SVG_NS = "{http://www.w3.org/2000/svg}"


class VisualContractError(ValueError):
    pass


def require(ok: bool, description: str) -> None:
    if not ok:
        raise VisualContractError(description)


def linear(component: int) -> float:
    s = component / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


def luminance(value: str) -> float:
    r, g, b = (int(value[i:i+2], 16) for i in (1, 3, 5))
    return .2126 * linear(r) + .7152 * linear(g) + .0722 * linear(b)


def contrast(foreground: str, background: str) -> float:
    top, bottom = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (top + 0.05) / (bottom + 0.05)


def validate_palette(doc: dict) -> dict:
    require(doc.get("schema") == "deputation.visual_palette.v1", "Invalid palette schema")
    colors = doc.get("colors")
    require(isinstance(colors, dict) and len(colors) == 16, "Palette must use exactly 16 colors")
    require(all(isinstance(v, str) and HEX.fullmatch(v) for v in colors.values()), "Invalid hex color")
    require(len(set(colors.values())) == 16, "Colors may not be duplicated")
    pairs = doc.get("text_pairings")
    require(isinstance(pairs, list) and len(pairs) >= 10, "Missing accessibility pairings")
    for pair in pairs:
        require(isinstance(pair, list) and len(pair) == 2, "Invalid text pair")
        fg, bg = pair
        require(fg in colors and bg in colors, f"Unknown text color pairing: {pair}")
        value = contrast(colors[fg], colors[bg])
        require(value >= 4.5, f"Low text contrast: {fg}/{bg} = {value:.2f}:1")
    for role, color in doc.get("semantic_roles", {}).items():
        require(color in colors, f"Role {role} maps to unknown color")
    require(doc.get("max_colors") == 16, "Max color budget changed")
    return {"colors": len(colors), "pairs": len(pairs)}


def validate_copy(doc: dict) -> dict:
    require(doc.get("schema") == "deputation.narrative_content.v1", "Invalid content schema")
    require(doc.get("case_id") == "EXP-0042", "Content case ID mismatch")
    require(isinstance(doc.get("premise"), str) and len(doc["premise"]) >= 50, "Missing premise")
    rooms = doc.get("room_descriptions", {})
    require(set(rooms) == {"COURTYARD", "REGISTRY", "ARCHIVE"}, "Room copy missing")
    actors = doc.get("actors")
    require(isinstance(actors, list) and len(actors) >= 4, "Actor copy missing")
    require(len({a["id"] for a in actors}) == len(actors), "Duplicate actor")
    for actor in actors:
        for key in ("name", "role", "motivation"):
            require(isinstance(actor.get(key), str) and len(actor[key]) >= 4,
                    f"Incomplete NPC motivation {actor}")
    results = doc.get("results", {})
    for code in ("BOOT", "MOVED", "CASE_FILE_READ", "PERMIT_GRANTED",
                 "ARCHIVE_READ", "CASE_VALIDATED", "DEADLINE_EXPIRED",
                 "CASE_ALREADY_VALIDATED", "STATUS_VIEWED"):
        require(code in results and all(results[code].get(k) for k in
                ("actor", "label", "message", "next", "cue")), f"Missing authored result {code}")
    require(set(doc.get("audio_events", {})) >= {"denial", "wait", "validate_case"},
            "Sound cue mapping missing")
    return {"actors": len(actors), "results": len(results)}


def validate_wireframes(directory: Path = WIREFRAMES) -> int:
    existing = {p.name for p in directory.glob("*.svg")}
    require(existing == EXPECTED, f"Expected exactly three source SVGs, got {existing}")
    for name in EXPECTED:
        doc = ET.parse(directory / name).getroot()
        require(doc.tag == SVG_NS + "svg", f"{name} not SVG")
        require(doc.attrib.get("viewBox") == "0 0 1280 720", f"{name} wrong canvas")
        labels = "".join(node.text or "" for node in doc.iter() if node.tag == SVG_NS + "text")
        for token in ("THE DEPUTATION", "EXP-0042", "SIMULADO"):
            require(token in labels, f"{name} missing always-on {token}")
        require(len(list(doc.iter(SVG_NS + "rect"))) >= 10, f"{name} lacks visual hierarchy")
    return len(EXPECTED)


def main() -> int:
    palette = validate_palette(json.loads(PALETTE.read_text(encoding="utf-8")))
    narrative = validate_copy(json.loads(CONTENT.read_text(encoding="utf-8")))
    wireframes = validate_wireframes()
    print(f"VISUAL PASS: {palette['colors']} colors, {palette['pairs']} accessible text pairs, "
          f"{narrative['actors']} actors, {narrative['results']} result texts, "
          f"{wireframes} original SVG wireframes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
