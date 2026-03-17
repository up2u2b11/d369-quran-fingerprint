"""
Experiment 05 — Special-6 at the Word Level
============================================
Question: How does the word-level digital root distribution differ
          between Special-6 and classical Abjad in the Quran?

Method:
  1. For each of 78,248 words: compute digital root under both systems
  2. Compare distributions (Chi-Square vs uniform)
  3. Identify which roots are dominant under each system

Finding: Each system reveals a different layer.
  - Abjad: root 9 dominates (14.0%), {3,6,9} = 38.2%
  - Special-6: root 5 dominates (13.1%), {3,6,9} = 34.2%

Intellectual property: Emad Suleiman Alwan — 2026
"""

import sqlite3
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import digit_root

DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")


def load_word_roots(db_path: str) -> tuple:
    """
    Load digital roots for all words under both Abjad and Special-6.
    Returns: (abjad_roots, special6_roots)
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT jummal_value, CAST(jummal_special_6 AS INTEGER)
        FROM words
        WHERE jummal_value > 0 AND jummal_special_6 != '0'
    """)
    rows = c.fetchall()
    conn.close()

    abjad_roots = [digit_root(r[0]) for r in rows]
    k6_roots = [digit_root(r[1]) for r in rows]
    return abjad_roots, k6_roots


def chi_square(distribution: dict, n: int) -> tuple:
    """Chi-Square test against uniform distribution (11.1% per root)."""
    try:
        from scipy import stats
        observed = [distribution.get(r, 0) for r in range(1, 10)]
        expected = [n / 9] * 9
        chi2, p = stats.chisquare(observed, expected)
        return chi2, p
    except ImportError:
        return None, None


def run(db_path: str = DB_PATH) -> dict:
    print("=" * 60)
    print("Experiment 05 — Special-6 vs Abjad at the Word Level")
    print("78,248 Quranic words")
    print("=" * 60)

    abjad_roots, k6_roots = load_word_roots(db_path)
    n = len(abjad_roots)

    abjad_cnt = Counter(abjad_roots)
    k6_cnt = Counter(k6_roots)

    # Summary
    abjad_369 = sum(abjad_cnt[r] for r in (3, 6, 9))
    k6_369 = sum(k6_cnt[r] for r in (3, 6, 9))

    print(f"\nWords analyzed: {n:,}")
    print(f"\n{'Root':>4} | {'Abjad':>7} | {'Abjad%':>6} | {'Special-6':>9} | {'S6%':>5}")
    print("─" * 45)
    for r in range(1, 10):
        mark = " ←" if r in (3, 6, 9) else ""
        print(f"   {r}  | {abjad_cnt[r]:>7} | {abjad_cnt[r]/n*100:>5.1f}% | {k6_cnt[r]:>9} | {k6_cnt[r]/n*100:>4.1f}%{mark}")

    print(f"\n{{3,6,9}} totals:")
    print(f"  Abjad:     {abjad_369:,} / {n:,} = {abjad_369/n*100:.1f}%")
    print(f"  Special-6: {k6_369:,} / {n:,} = {k6_369/n*100:.1f}%")

    # Chi-Square
    a_chi2, a_p = chi_square(abjad_cnt, n)
    k_chi2, k_p = chi_square(k6_cnt, n)
    print(f"\nChi-Square (vs uniform 11.1% per root):")
    if a_chi2:
        print(f"  Abjad:     χ²={a_chi2:.1f}  p≈{a_p:.0e}  {'✅' if a_p<0.05 else '✗'}")
    if k_chi2:
        print(f"  Special-6: χ²={k_chi2:.1f}  p≈{k_p:.0e}  {'✅' if k_p<0.05 else '✗'}")

    # Key insight
    abjad_peak = max(range(1, 10), key=lambda r: abjad_cnt[r])
    k6_peak = max(range(1, 10), key=lambda r: k6_cnt[r])
    print(f"\nPeak root — Abjad: {abjad_peak}  |  Special-6: {k6_peak}")
    print("→ Each system reveals a different layer of the text.")

    return {
        "n": n,
        "abjad": {"count_369": abjad_369, "pct": abjad_369/n*100, "distribution": dict(abjad_cnt)},
        "special6": {"count_369": k6_369, "pct": k6_369/n*100, "distribution": dict(k6_cnt)},
    }


if __name__ == "__main__":
    run()
