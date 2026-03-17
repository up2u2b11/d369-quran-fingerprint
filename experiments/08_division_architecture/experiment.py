"""
Experiment 08 — The Architecture of Division (Gate Five)
=========================================================
The fundamental question: Is the {3,6,9} fingerprint produced by the
specific Surah lengths — or would any division of the words show it?

Methodology:
  - Encoding: Special-6 (jummal_special_6 column from database)
  - Value definition: sum of KHASS_6 letter values per word (pre-computed in DB)
  - Basmala: INCLUDED in Surah 1 (al-Fatiha = 29 words, including the Basmala)
  - All 4 tests operate on the same 78,248 words in original Quranic order

Four tests:
  A — Real Surahs (114 Surahs with their actual unequal lengths) [reference]
  B — Equal division (114 chunks of ~687 words each)
  C — Random division × 1,000 (distribution of any possible 114-way split)
  D — Individual verses (6,236 ayat as independent units)

Intellectual property: Emad Suleiman Alwan — March 17, 2026
"""

import sqlite3
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import digit_root

DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")


def load_data(db_path: str) -> tuple:
    """Load Special-6 values, Surah sizes, and verse sizes."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT CAST(jummal_special_6 AS INTEGER) FROM words ORDER BY word_pos_in_quran")
    vals = [r[0] for r in c.fetchall()]

    c.execute("SELECT surah_id, COUNT(*) FROM words GROUP BY surah_id ORDER BY surah_id")
    surah_sizes = [r[1] for r in c.fetchall()]

    c.execute("""SELECT surah_id, ayah_number, COUNT(*)
                 FROM words GROUP BY surah_id, ayah_number
                 ORDER BY surah_id, ayah_number""")
    ayah_sizes = [r[2] for r in c.fetchall()]

    conn.close()
    return vals, surah_sizes, ayah_sizes


def count_369(vals: list, sizes: list) -> int:
    """Count units whose Special-6 sum has a digital root in {3, 6, 9}."""
    idx = count = 0
    for sz in sizes:
        if digit_root(sum(vals[idx:idx+sz])) in (3, 6, 9):
            count += 1
        idx += sz
    return count


def perm_test(vals: list, sizes: list, observed: int, trials: int = 10_000) -> float:
    """Permutation test: shuffle word values, recompute, count exceedances."""
    v = vals.copy()
    exceed = 0
    for _ in range(trials):
        random.shuffle(v)
        if count_369(v, sizes) >= observed:
            exceed += 1
    return exceed / trials


def run(db_path: str = DB_PATH) -> dict:
    print("=" * 65)
    print("Experiment 08 — The Architecture of Division (Gate Five)")
    print("=" * 65)
    print("\nMethodology:")
    print("  System:   Special-6 (jummal_special_6 column from database)")
    print("  Basmala:  Included in Surah 1 (surah_id=1, 29 words)")
    print("  Words:    78,248 words in original Quranic order")

    vals, surah_sizes, ayah_sizes = load_data(db_path)
    N = len(vals)
    print(f"\nLoaded: {N:,} words | {len(surah_sizes)} Surahs | {len(ayah_sizes):,} verses")

    # Test A — Real Surahs
    print(f"\n{'─'*55}")
    print("Test A — Real Surahs (114 Surahs, actual unequal lengths)")
    obs_A = count_369(vals, surah_sizes)
    print(f"   {{3,6,9}} = {obs_A}/114 = {obs_A/114*100:.1f}%  — running permutation test (10,000)...")
    p_A = perm_test(vals, surah_sizes, obs_A, 10_000)
    print(f"   p = {p_A:.4f}  {'✅ significant' if p_A < 0.05 else '✗ not significant'}")

    # Test B — Equal division
    print(f"\n{'─'*55}")
    print("Test B — Equal division (114 × ~687 words)")
    chunk = N // 114
    equal_sizes = [chunk] * 113 + [N - chunk * 113]
    obs_B = count_369(vals, equal_sizes)
    print(f"   Chunk size: {chunk} words")
    print(f"   {{3,6,9}} = {obs_B}/114 = {obs_B/114*100:.1f}%  — running permutation test (10,000)...")
    p_B = perm_test(vals, equal_sizes, obs_B, 10_000)
    print(f"   p = {p_B:.4f}  {'✅ significant' if p_B < 0.05 else '✗ not significant'}")

    # Test C — Random division × 1,000
    print(f"\n{'─'*55}")
    print("Test C — Random division × 1,000")
    random_counts = []
    for _ in range(1_000):
        cuts = sorted(random.sample(range(1, N), 113))
        sizes_r = ([cuts[0]]
                   + [cuts[i] - cuts[i-1] for i in range(1, 113)]
                   + [N - cuts[-1]])
        random_counts.append(count_369(vals, sizes_r))
    random_counts.sort()
    median_C = random_counts[500]
    pct_A = sum(1 for x in random_counts if x < obs_A) / 10
    threshold_95 = random_counts[950]
    print(f"   Median:        {median_C}/114 = {median_C/114*100:.1f}%")
    print(f"   95th percentile: {threshold_95}/114")
    print(f"   Real Surahs ({obs_A}) exceed {pct_A:.1f}% of all random divisions")
    print(f"   Distribution: min={random_counts[0]} | Q25={random_counts[250]} | med={median_C} | Q75={random_counts[750]} | max={random_counts[-1]}")

    # Test D — Verses
    print(f"\n{'─'*55}")
    print(f"Test D — Individual verses ({len(ayah_sizes):,} ayat)")
    obs_D = count_369(vals, ayah_sizes)
    print(f"   {{3,6,9}} = {obs_D}/{len(ayah_sizes)} = {obs_D/len(ayah_sizes)*100:.1f}%  — running permutation test (5,000)...")
    p_D = perm_test(vals, ayah_sizes, obs_D, 5_000)
    print(f"   p = {p_D:.4f}  {'✅ significant' if p_D < 0.05 else '✗ not significant'}")

    # Summary table
    print(f"\n{'='*65}")
    print(f"{'Division':<24} {'Units':>6} {'{{3,6,9}}':>8} {'Pct':>7} {'p-value':>10}")
    print("─" * 65)
    print(f"  {'A: Real Surahs':<22} {114:>6} {obs_A:>8} {obs_A/114*100:>6.1f}% {p_A:>10.4f}  {'✅' if p_A<0.05 else '✗'}")
    print(f"  {'B: Equal (~687 words)':<22} {114:>6} {obs_B:>8} {obs_B/114*100:>6.1f}% {p_B:>10.4f}  {'✅' if p_B<0.05 else '✗'}")
    print(f"  {'C: Random (median)':<22} {114:>6} {median_C:>8} {median_C/114*100:>6.1f}% {'—':>10}  ({obs_A} at {pct_A:.0f}th percentile)")
    print(f"  {'D: Verses':<22} {len(ayah_sizes):>6} {obs_D:>8} {obs_D/len(ayah_sizes)*100:>6.1f}% {p_D:>10.4f}  {'✅' if p_D<0.05 else '✗'}")
    print("=" * 65)

    # Verdict
    print("\nVerdict:")
    if p_A < 0.05 and p_B >= 0.05 and pct_A >= 95:
        verdict = "Fingerprint is in the ARCHITECTURE — the specific Surah lengths are the design"
    elif p_A < 0.05 and p_B < 0.05:
        verdict = "Fingerprint is in the VOCABULARY — any division reveals it"
    else:
        verdict = "Composite result — requires deeper analysis"
    print(f"→ {verdict}")
    if p_D < 0.05:
        print(f"  + Fingerprint is present even at verse level ({obs_D}/{len(ayah_sizes)} = {obs_D/len(ayah_sizes)*100:.1f}%)")

    return {
        "A": {"obs": obs_A, "n": 114, "p": p_A},
        "B": {"obs": obs_B, "n": 114, "p": p_B},
        "C": {"median": median_C, "percentile_A": pct_A, "threshold_95": threshold_95},
        "D": {"obs": obs_D, "n": len(ayah_sizes), "p": p_D},
    }


if __name__ == "__main__":
    run()
