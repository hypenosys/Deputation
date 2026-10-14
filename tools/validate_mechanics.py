#!/usr/bin/env python3
"""Validate THE DEPUTATION's extracted mechanics and their authored contracts.

All-source metadata belongs to ABBI, not to the new Deputation repository.
Status values are source-inspection claims, never runtime certification.
No external Python dependencies required.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/mechanics/extraction.v1.json"
CONTRACTS = ROOT / "data/mechanics/contracts.v1.json"
WORLD = ROOT / "data/world/vertical_slice.v1.json"
LEVELS = {"c64_source", "c_module_not_wired", "host_prototype", "design_goal"}
ID = re.compile(r"DPT-M-\d{3}\Z")
CONTRACT_ID = re.compile(r"DPT-C-\d{3}\Z")
ABBI_ID = re.compile(r"ABBI-M-\d{6}\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")


class CatalogError(ValueError):
    """Catalog or contract violates repository invariants."""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(predicate: bool, message: str) -> None:
    if not predicate:
        raise CatalogError(message)


def validate_catalog(data: dict) -> Counter:
    require(data.get("schema") == "deputation.extraction.v1", "Invalid extraction schema")
    require(data.get("repository") == "hypenosys/abbi", "Extraction provenance repository changed")
    require(bool(SHA.fullmatch(str(data.get("observed_git_sha", "")))), "Missing exact source commit SHA")
    entries = data.get("mechanics")
    require(isinstance(entries, list) and entries, "No mechanics")
    ids = set()
    counts: Counter = Counter()
    for entry in entries:
        mid = entry.get("id")
        require(isinstance(mid, str) and bool(ID.fullmatch(mid)), "Invalid DPT ID")
        require(mid not in ids, f"Duplicate ID: {mid}")
        ids.add(mid)
        level = entry.get("evidence_level")
        require(level in LEVELS, f"{mid}: unknown evidence level")
        counts[level] += 1
        require(isinstance(entry.get("name"), str) and len(entry["name"].strip()) >= 5, f"{mid}: missing name")
        require(isinstance(entry.get("description"), str) and len(entry["description"].strip()) >= 25, f"{mid}: inadequate description")
        sources = entry.get("source_paths")
        require(isinstance(sources, list) and len(sources) > 0, f"{mid}: missing sources")
        for src in sources:
            require(isinstance(src, str) and bool(src), f"{mid}: invalid path")
            p = PurePosixPath(src)
            require(not p.is_absolute() and ".." not in p.parts and "\\" not in src, f"{mid}: unsafe source path")
        relation = entry.get("abbi_candidate_relation")
        require(relation is None or (isinstance(relation, str) and bool(ABBI_ID.fullmatch(relation))), f"{mid}: invalid ABBI relation")
    expected = [f"DPT-M-{i:03d}" for i in range(1, len(entries) + 1)]
    require(sorted(ids) == expected, "Extraction ID sequence must remain contiguous and immutable")
    require(dict(counts) == {k: v for k, v in data.get("counts", {}).items() if v}, "Evidence totals out of sync")
    return counts


def validate_contracts(document: dict, catalog: dict) -> int:
    require(document.get("schema") == "deputation.mechanic_contracts.v1", "Contract schema invalid")
    ids = {x["id"]: x for x in catalog["mechanics"]}
    seen = set()
    items = document.get("contracts", [])
    require(isinstance(items, list) and items, "No contracts")
    for contract in items:
        cid, mid = contract.get("id"), contract.get("mechanic_id")
        require(isinstance(cid, str) and bool(CONTRACT_ID.fullmatch(cid)), "Invalid contract ID")
        require(cid not in seen, f"Duplicate contract {cid}")
        seen.add(cid)
        require(mid in ids, f"Unknown mechanic for {cid}")
        require(cid[-3:] == mid[-3:], f"{cid} must refer to matching mechanic ID")
        require(contract.get("evidence_level") == ids[mid]["evidence_level"], f"{cid}: false evidence promotion")
        require(contract.get("status") == "documented_contract", f"{cid}: unsupported implementation claim")
        for field in ("inputs", "outputs", "invariants"):
            values = contract.get(field)
            require(isinstance(values, list) and all(isinstance(v, str) and len(v.strip()) > 5 for v in values) and values, f"{cid}: empty {field}")
        verification = contract.get("platform_verification", {})
        require(set(verification) == {"godot", "host", "vice", "c64_ultimate"}, f"{cid}: missing platform")
        require(all(value == "not_run" for value in verification.values()), f"{cid}: runtime evidence cannot be asserted in a contract draft")
    return len(items)


def validate_world(world: dict) -> int:
    require(world.get("schema") == "deputation.world.v1", "World schema invalid")
    rooms = world.get("rooms", [])
    require(isinstance(rooms, list) and len(rooms) >= 3, "Insufficient world rooms")
    by_id = {r["id"]: r for r in rooms}
    require(len(by_id) == len(rooms), "Duplicate room IDs")
    for room in rooms:
        exits = room.get("exits", [])
        minutes = room.get("travel_minutes", [])
        require(len(exits) <= len(minutes), "Travel cost slots missing")
        require(len(set(exits)) == len(exits), "Duplicate exits")
        require(len(room.get("camera_anchor", [])) == 3, "Camera anchor invalid")
        for i, destination in enumerate(exits):
            require(destination in by_id, "Dangling room exit")
            require(room["id"] in by_id[destination].get("exits", []), "Non-reciprocal room exit")
            require(isinstance(minutes[i], int) and minutes[i] > 0, "Travel time must be positive")
    route = world.get("route", [])
    require(route and all(v in by_id for v in route), "Invalid reference route")
    for start, dest in zip(route, route[1:]):
        require(dest in by_id[start]["exits"], "Route jumps across nonadjacent rooms")
    return len(rooms)


def main() -> int:
    try:
        catalog, contracts, world = load_json(CATALOG), load_json(CONTRACTS), load_json(WORLD)
        totals = validate_catalog(catalog)
        contract_count = validate_contracts(contracts, catalog)
        room_count = validate_world(world)
    except (CatalogError, OSError, ValueError, KeyError, TypeError) as err:
        print(f"VALIDATION FAIL: {err}", file=sys.stderr)
        return 1
    print(f"VALIDATION PASS: {sum(totals.values())} observations, {contract_count} contracts, {room_count} rooms")
    print("EVIDENCE:", ", ".join(f"{key}={totals[key]}" for key in sorted(LEVELS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
