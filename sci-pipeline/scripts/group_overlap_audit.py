#!/usr/bin/env python3
"""Audit split manifests for shared independent units (stdlib only).

Input: one CSV with a split column, or several CSVs (one per split, split name = file stem).
Checks, per pair of splits:
  - identical unit ids after normalization (strip + casefold), and ids that differ
    only by whitespace/case (a sign of an unnormalized key, not of independence)
  - shared cluster ids (e.g. family, site) when --cluster-col is given
  - overlapping time intervals when --time-col is given (ISO-8601); counted as a
    failure only with --temporal (participant-level splits normally overlap in time)

Exit code 1 if any overlap is found, 0 otherwise.
No overlap is NOT proof of independence; an overlap is NOT proof of model leakage.

Idea adapted from exploratory-data-analysis/scripts/missingness_leakage_audit.py in
K-Dense-AI/claude-scientific-skills (MIT); independent stdlib rewrite with cluster checks.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path


def norm(x: str) -> str:
    return x.strip().casefold()


def read_rows(paths: list[Path], split_col: str | None) -> dict[str, list[dict]]:
    by_split: dict[str, list[dict]] = defaultdict(list)
    for p in paths:
        with p.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if split_col:
                    if split_col not in row:
                        raise SystemExit(f"ERROR: column {split_col!r} not in {p}")
                    by_split[row[split_col]].append(row)
                else:
                    by_split[p.stem].append(row)
    return by_split


def parse_time(s: str) -> datetime:
    return datetime.fromisoformat(s.strip().replace("Z", "+00:00"))


def audit(by_split, unit_col, cluster_col, time_col, temporal=False) -> dict:
    report: dict = {"splits": {k: len(v) for k, v in by_split.items()}, "pairs": [],
                    "caveats": ["no overlap found is not proof of independence",
                                "an overlap is not proof of model leakage"]}
    for name, rows in by_split.items():
        if rows and unit_col not in rows[0]:
            raise SystemExit(f"ERROR: unit column {unit_col!r} missing in split {name!r}")
    for a, b in combinations(sorted(by_split), 2):
        ra, rb = by_split[a], by_split[b]
        raw_a = {r[unit_col] for r in ra}
        raw_b = {r[unit_col] for r in rb}
        na = defaultdict(set)
        nb = defaultdict(set)
        for v in raw_a:
            na[norm(v)].add(v)
        for v in raw_b:
            nb[norm(v)].add(v)
        shared = sorted(set(na) & set(nb))
        variant_only = sorted(k for k in shared if not (na[k] & nb[k]))
        pair = {"pair": [a, b], "shared_units": len(shared),
                "shared_units_example": shared[:5],
                "shared_only_after_normalization": len(variant_only),
                "variant_example": [[sorted(na[k]), sorted(nb[k])] for k in variant_only[:3]]}
        if cluster_col:
            ca = {norm(r[cluster_col]) for r in ra if r.get(cluster_col, "").strip()}
            cb = {norm(r[cluster_col]) for r in rb if r.get(cluster_col, "").strip()}
            sc = sorted(ca & cb)
            pair["shared_clusters"] = len(sc)
            pair["shared_clusters_example"] = sc[:5]
        if time_col:
            ta = [parse_time(r[time_col]) for r in ra if r.get(time_col, "").strip()]
            tb = [parse_time(r[time_col]) for r in rb if r.get(time_col, "").strip()]
            if ta and tb:
                lo, hi = max(min(ta), min(tb)), min(max(ta), max(tb))
                pair["time_interval_overlap"] = lo <= hi
                pair["time_ranges"] = [[min(ta).isoformat(), max(ta).isoformat()],
                                       [min(tb).isoformat(), max(tb).isoformat()]]
        report["pairs"].append(pair)
    report["overlap_found"] = any(
        p["shared_units"] or p.get("shared_clusters") or (temporal and p.get("time_interval_overlap"))
        for p in report["pairs"])
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+", type=Path)
    ap.add_argument("--unit-col", required=True, help="independent unit id column (e.g. participant_id)")
    ap.add_argument("--split-col", help="split column when a single CSV holds all splits")
    ap.add_argument("--cluster-col", help="cluster id column (e.g. family_id, site)")
    ap.add_argument("--time-col", help="ISO-8601 time column; reports interval overlap between splits")
    ap.add_argument("--temporal", action="store_true",
                    help="splits are meant to be time-separated: count time overlap as a failure")
    args = ap.parse_args(argv)
    by_split = read_rows(args.csv, args.split_col)
    if len(by_split) < 2:
        print("ERROR: need at least two splits")
        return 2
    report = audit(by_split, args.unit_col, args.cluster_col, args.time_col, args.temporal)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["overlap_found"] else 0


if __name__ == "__main__":
    sys.exit(main())
