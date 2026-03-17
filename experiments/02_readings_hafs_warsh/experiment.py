"""
Experiment 02 — Fingerprint Stability: Hafs vs Warsh
=====================================================
Question: Does the {3, 6, 9} fingerprint survive when switching
          from the Hafs reading to the Warsh reading of the Quran?

Method:
  1. Compute Abjad sums per Surah for Hafs (from database)
  2. Compute Abjad sums per Surah for Warsh (from text file)
  3. Compare:
     a) Total Abjad values and relative difference
     b) Transformation maps for both readings
     c) Which roots are stable in each reading?

Expected result:
  - Total difference < 0.01%
  - {3, 9} stable in both readings
  - {6} protected by different mechanisms in each reading

Intellectual property: Emad Suleiman Alwan — 2026
"""

import sqlite3
import re
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import JUMMAL_5, digit_root

DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")
WARSH_PATH = os.environ.get("WARSH_PATH", "/home/emad/quran_warsh.txt")


def load_hafs_by_surah(db_path: str) -> dict:
    """Load Hafs Abjad sums from the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT surah_id, text_uthmani FROM words ORDER BY surah_id, word_pos_in_quran")
    rows = c.fetchall()
    conn.close()

    sums = defaultdict(int)
    for surah_id, text in rows:
        sums[surah_id] += sum(JUMMAL_5.get(ch, 0) for ch in text)
    return dict(sums)


def load_warsh_by_surah(warsh_path: str) -> dict:
    """
    Load Warsh Abjad sums from a text file.
    Expected format: surah_id|ayah_number|text
    """
    try:
        with open(warsh_path, encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"  ⚠️  Warsh file not found: {warsh_path}")
        return {}

    sums = defaultdict(int)
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) >= 3:
            try:
                surah_id = int(parts[0])
                text = parts[2]
                sums[surah_id] += sum(JUMMAL_5.get(ch, 0) for ch in text)
            except (ValueError, IndexError):
                continue
    return dict(sums)


def transformation_map(surah_sums: dict) -> dict:
    """Build digital root transformation map for a set of Surah sums."""
    groups = defaultdict(int)
    counts = defaultdict(int)
    for sid, total in surah_sums.items():
        dr = digit_root(total)
        groups[dr] += total
        counts[dr] += 1
    return {dr: {"group_sum": groups[dr], "group_dr": digit_root(groups[dr]),
                 "count": counts[dr], "preserves": digit_root(groups[dr]) == dr}
            for dr in range(1, 10)}


def run(db_path: str = DB_PATH, warsh_path: str = WARSH_PATH) -> dict:
    print("=" * 60)
    print("Experiment 02 — Fingerprint Stability: Hafs vs Warsh")
    print("=" * 60)

    hafs = load_hafs_by_surah(db_path)
    warsh = load_warsh_by_surah(warsh_path)

    total_hafs = sum(hafs.values())
    total_warsh = sum(warsh.values()) if warsh else 0

    print(f"\nHafs total Abjad:  {total_hafs:,}  → root {digit_root(total_hafs)}")
    if warsh:
        diff = abs(total_hafs - total_warsh)
        pct = diff / total_hafs * 100
        print(f"Warsh total Abjad: {total_warsh:,}  → root {digit_root(total_warsh)}")
        print(f"Difference: {diff:,} ({pct:.4f}%)")

    # Hafs transformation map
    hafs_map = transformation_map(hafs)
    print(f"\n{'─'*50}")
    print("Transformation Map — Hafs")
    print(f"{'─'*50}")
    hafs_stable = set()
    for dr in range(1, 10):
        info = hafs_map[dr]
        mark = "✅ stable" if info["preserves"] else f"→ {info['group_dr']}"
        if info["preserves"]:
            hafs_stable.add(dr)
        print(f"  Root {dr} ({info['count']} Surahs): → {info['group_dr']}  {mark}")
    print(f"  Stable: {sorted(hafs_stable)}")

    # Warsh transformation map
    if warsh:
        warsh_map = transformation_map(warsh)
        print(f"\n{'─'*50}")
        print("Transformation Map — Warsh")
        print(f"{'─'*50}")
        warsh_stable = set()
        for dr in range(1, 10):
            info = warsh_map[dr]
            mark = "✅ stable" if info["preserves"] else f"→ {info['group_dr']}"
            if info["preserves"]:
                warsh_stable.add(dr)
            print(f"  Root {dr} ({info['count']} Surahs): → {info['group_dr']}  {mark}")
        print(f"  Stable: {sorted(warsh_stable)}")

        common = hafs_stable & warsh_stable
        print(f"\nShared stable roots (both readings): {sorted(common)}")

    return {"hafs_total": total_hafs, "hafs_stable": sorted(hafs_stable)}


if __name__ == "__main__":
    run()
