#!/usr/bin/env python3
"""Freeze and verify an experiment card by SHA-256 (stdlib only).

freeze <card>  : write <card>.sha256 next to the card. Refuses if a different
                 hash is already frozen (changing a frozen card needs a new card id).
                 With --strict, refuses when required fields are still "UNSET".
verify <card>  : exit 0 if the card matches its frozen hash, 1 otherwise.
                 --expect <sha> also checks an external anchor (commit the hash; a
                 sidecar in the same writable folder alone does not stop re-freezing).
unset <card>   : list fields whose value is still "UNSET" (exit 0).

Structure follows the "refuse on mismatch with existing snapshot" idea of
freeze_experiment_contract.py in MagicalLiHua/conduct-deep-learning-research (MIT);
this file is an independent rewrite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# Fields that must be decided before a confirmatory run (--strict).
STRICT_REQUIRED = [
    "research_mode", "primary_question", "independent_unit", "baseline",
    "single_changed_factor", "primary_estimand", "primary_metric", "direction",
    "minimum_effect_of_interest", "uncertainty_method", "multiplicity",
    "search_budget", "seed_policy", "stop_rules", "verdict_rule", "reviewer",
    "missingness", "input_allowlist", "split", "prediction_time_and_horizon",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


HASH_FILE: Path | None = None


def hash_path(card: Path) -> Path:
    return HASH_FILE if HASH_FILE else card.with_name(card.name + ".sha256")


def unset_fields(obj, prefix: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("_"):
                continue
            found += unset_fields(v, f"{prefix}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += unset_fields(v, f"{prefix}{i}.")
    elif obj == "UNSET":
        found.append(prefix.rstrip("."))
    return found


def load_card(card: Path) -> tuple[bytes, dict]:
    data = card.read_bytes()
    try:
        parsed = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {card} is not valid UTF-8 JSON: {exc}")
    if not isinstance(parsed, dict):
        raise SystemExit(f"ERROR: {card} must be a JSON object")
    return data, parsed


def cmd_freeze(card: Path, strict: bool) -> int:
    data, parsed = load_card(card)
    mode = parsed.get("research_mode")
    mode = mode.get("value") if isinstance(mode, dict) else mode
    if mode in ("CONFIRMATORY", "REPLICATION") and not strict:
        strict = True
        print("note: research_mode is", mode, "-> --strict enforced")
    if strict:
        unset = unset_fields(parsed)
        blocking = sorted({f for f in unset if f.split(".")[0] in STRICT_REQUIRED})
        if blocking:
            print("REFUSED: required fields still UNSET:\n  " + "\n  ".join(blocking))
            return 1
    digest = sha256_bytes(data)
    hp = hash_path(card)
    if hp.exists():
        prev = hp.read_text(encoding="utf-8").split()[0]
        if prev != digest:
            print(f"REFUSED: {card} already frozen as {prev[:12]}…; current content is {digest[:12]}…\n"
                  "A frozen card is not edited. Create a new card id (and record why).")
            return 1
        print(json.dumps({"status": "already_frozen", "sha256": digest}))
        return 0
    hp.write_text(f"{digest}  {card.name}\n", encoding="utf-8")
    print(json.dumps({"status": "frozen", "sha256": digest, "hash_file": str(hp),
                      "unset_fields": unset_fields(parsed)}, ensure_ascii=False))
    return 0


def cmd_verify(card: Path) -> int:
    hp = hash_path(card)
    if not hp.exists():
        print(f"FAIL: no frozen hash at {hp}")
        return 1
    expected = hp.read_text(encoding="utf-8").split()[0]
    actual = sha256_bytes(card.read_bytes())
    if actual != expected:
        print(f"FAIL: {card} changed after freezing (frozen {expected[:12]}…, now {actual[:12]}…)")
        return 1
    print(f"OK: {card} matches frozen sha256 {expected}")
    return 0


def cmd_unset(card: Path) -> int:
    _, parsed = load_card(card)
    fields = unset_fields(parsed)
    print("\n".join(fields) if fields else "(no UNSET fields)")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["freeze", "verify", "unset"])
    ap.add_argument("card", type=Path)
    ap.add_argument("--strict", action="store_true", help="refuse freezing while required fields are UNSET")
    ap.add_argument("--hash-file", type=Path, help="existing hash sidecar path (default: <card>.sha256)")
    ap.add_argument("--expect", help="expected sha256 from an external anchor (e.g. the committed value); verify fails on mismatch")
    args = ap.parse_args(argv)
    global HASH_FILE
    HASH_FILE = args.hash_file
    if not args.card.is_file():
        print(f"ERROR: {args.card} not found")
        return 2
    if args.command == "freeze":
        return cmd_freeze(args.card, args.strict)
    if args.command == "verify":
        if args.expect:
            actual = sha256_bytes(args.card.read_bytes())
            if actual != args.expect.strip().lower():
                print(f"FAIL: {args.card} sha256 {actual[:12]}… != external anchor {args.expect[:12]}…")
                return 1
        return cmd_verify(args.card)
    return cmd_unset(args.card)


if __name__ == "__main__":
    sys.exit(main())
