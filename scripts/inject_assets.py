#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
import struct
from pathlib import Path
from typing import Iterable

MARKET_KEYS = [
    "floor", "wall", "wall-window", "column", "shelf-bags", "shelf-boxes",
    "shelf-end", "display-fruit", "display-bread", "freezer",
    "freezers-standing", "fence", "cash-register", "shopping-cart",
    "shopping-basket", "bottle-return",
]
CHARACTER_KEYS = [
    "character-employee", "char-female-a", "char-female-b", "char-female-c",
    "char-male-a", "char-male-b", "char-male-c",
]
FOOD_NAMES = [
    "apple", "banana", "bread", "cheese", "carton", "can", "bag",
    "bottle-ketchup", "broccoli", "carrot", "cake", "cookie", "chocolate",
    "bowl-cereal", "bacon", "avocado",
]
BUILDING_NAMES = [
    "floor", "wall", "wall-window-square", "wall-doorway-square",
    "roof-flat-square",
]


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower().replace("(clone)", ""))


def glb_names(path: Path) -> set[str]:
    """Return normalized scene/node/mesh names from a GLB file."""
    names: set[str] = set()
    try:
        data = path.read_bytes()
        if len(data) < 20 or data[:4] != b"glTF":
            return names
        json_len, chunk_type = struct.unpack_from("<I4s", data, 12)
        if chunk_type != b"JSON":
            return names
        raw = data[20 : 20 + json_len].decode("utf-8").rstrip("\x00 ")
        doc = json.loads(raw)
        for group in ("scenes", "nodes", "meshes"):
            for item in doc.get(group, []):
                name = item.get("name")
                if name:
                    names.add(normalize(name))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, struct.error):
        pass
    return names


def all_glbs(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() == ".glb")


def find_glb(root: Path, expected_name: str) -> Path:
    expected = normalize(expected_name)
    candidates = all_glbs(root)
    if not candidates:
        raise FileNotFoundError(f"Aucun fichier GLB trouvé dans {root}")

    ranked: list[tuple[int, int, Path]] = []
    for path in candidates:
        stem = normalize(path.stem)
        score = 0
        if stem == expected:
            score = 100
        elif expected in glb_names(path):
            score = 90
        elif stem.endswith(expected) or expected.endswith(stem):
            score = 50
        if score:
            ranked.append((score, -len(str(path)), path))

    if not ranked:
        preview = ", ".join(p.stem for p in candidates[:20])
        raise FileNotFoundError(
            f"Modèle '{expected_name}' introuvable dans {root}. Exemples présents : {preview}"
        )
    ranked.sort(reverse=True)
    return ranked[0][2]


def encode(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def add_group(
    output: dict[str, str], root: Path, mappings: Iterable[tuple[str, str]]
) -> None:
    for output_key, source_name in mappings:
        found = find_glb(root, source_name)
        output[output_key] = encode(found)
        print(f"✓ {output_key}: {found}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--market", type=Path, required=True)
    parser.add_argument("--characters", type=Path, required=True)
    parser.add_argument("--food", type=Path, required=True)
    parser.add_argument("--building", type=Path, required=True)
    parser.add_argument("--furniture", type=Path, required=True)
    args = parser.parse_args()

    assets: dict[str, str] = {}
    add_group(assets, args.market, ((name, name) for name in MARKET_KEYS))
    add_group(assets, args.characters, ((name, name) for name in CHARACTER_KEYS))
    add_group(assets, args.food, ((f"food-{name}", name) for name in FOOD_NAMES))
    add_group(assets, args.building, ((f"bld-{name}", name) for name in BUILDING_NAMES))
    add_group(assets, args.furniture, (("lamp-round-floor", "lamp-round-floor"),))

    template = args.template.read_text(encoding="utf-8")
    marker = "__ASSET_B64__"
    if template.count(marker) != 1:
        raise RuntimeError(f"Le marqueur {marker} doit apparaître exactement une fois")

    rendered = template.replace(marker, json.dumps(assets, separators=(",", ":")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"✓ Jeu restauré : {args.output} ({len(assets)} modèles)")


if __name__ == "__main__":
    main()
