"""
Experiment 06 — Special-6 Transformation Map (vs Abjad)
========================================================
Question: Does the group-sum transformation map behave the same way
          under Special-6 as under Abjad (G14)?

Method:
  1. For each Surah: compute Special-6 sum → digital root
  2. Group Surahs by digital root (9 groups)
  3. Sum each group, compute digital root of the sum
  4. Compare with the Abjad (G14) transformation map

Finding:
  - Abjad (G14): {3, 6, 9} all stable
  - Special-6: only {9} stable
  - But both agree on {9}

Intellectual property: Emad Suleiman Alwan — 2026
"""

import sqlite3
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import JUMMAL_5, KHASS_6, digit_root

DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")


def load_surah_sums_abjad(db_path: str) -> dict:
    """Load Abjad sums per Surah (ة=5), computed from text_uthmani."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT surah_id, text_uthmani FROM words ORDER BY surah_id, word_pos_in_quran")
    rows = c.fetchall()
    conn.close()
    sums = defaultdict(int)
    for sid, text in rows:
        sums[sid] += sum(JUMMAL_5.get(ch, 0) for ch in text)
    return dict(sums)


def load_surah_sums_k6(db_path: str) -> dict:
    """Load Special-6 sums per Surah from the database column."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT surah_id, CAST(jummal_special_6 AS INTEGER)
        FROM words
        WHERE jummal_special_6 != '0'
        ORDER BY surah_id, word_pos_in_quran
    """)
    rows = c.fetchall()
    conn.close()
    sums = defaultdict(int)
    for sid, val in rows:
        sums[sid] += val
    return dict(sums)


def build_map(surah_sums: dict) -> dict:
    """Build transformation map: root → root of group sum."""
    groups = defaultdict(lambda: {"sum": 0, "count": 0})
    for sid, total in sorted(surah_sums.items()):
        dr = digit_root(total)
        groups[dr]["sum"] += total
        groups[dr]["count"] += 1
    return {dr: {
        "count": groups[dr]["count"],
        "group_sum": groups[dr]["sum"],
        "group_dr": digit_root(groups[dr]["sum"]),
        "preserves": digit_root(groups[dr]["sum"]) == dr
    } for dr in range(1, 10)}


def run(db_path: str = DB_PATH) -> dict:
    print("=" * 65)
    print("Experiment 06 — Transformation Maps: Abjad vs Special-6")
    print("=" * 65)

    abjad_sums = load_surah_sums_abjad(db_path)
    k6_sums = load_surah_sums_k6(db_path)

    abjad_map = build_map(abjad_sums)
    k6_map = build_map(k6_sums)

    print(f"\n{'Root':>4} | {'Abjad →':>8} | {'Stable?':>7} | {'Special-6 →':>11} | {'Stable?':>7} | {'Match?':>6}")
    print("─" * 60)

    abjad_stable = set()
    k6_stable = set()

    for dr in range(1, 10):
        a_gdr = abjad_map[dr]["group_dr"]
        k_gdr = k6_map[dr]["group_dr"]
        a_stab = "✅" if abjad_map[dr]["preserves"] else "✗"
        k_stab = "✅" if k6_map[dr]["preserves"] else "✗"
        match = "✅" if a_gdr == k_gdr else "✗"
        if abjad_map[dr]["preserves"]:
            abjad_stable.add(dr)
        if k6_map[dr]["preserves"]:
            k6_stable.add(dr)
        print(f"   {dr}  |     → {a_gdr}    |   {a_stab}    |      → {k_gdr}      |   {k_stab}    |   {match}")

    print(f"\nAbjad stable:     {sorted(abjad_stable)}")
    print(f"Special-6 stable: {sorted(k6_stable)}")
    print(f"Shared:           {sorted(abjad_stable & k6_stable)}")
    print(f"\n→ Both systems agree on {{9}} as a stable root.")
    print(f"  Abjad additionally shows {{3, 6}} stability.")

    return {
        "abjad_stable": sorted(abjad_stable),
        "k6_stable": sorted(k6_stable),
        "shared": sorted(abjad_stable & k6_stable)
    }


if __name__ == "__main__":
    run()
