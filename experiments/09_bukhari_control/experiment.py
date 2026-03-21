"""
Experiment 09 — Bukhari as Control Group (Gate Six)
====================================================
Question: Is the fingerprint unique to the Quran — or shared by any
          classical Arabic religious text?

Logic: Bukhari is Arabic, religious, about the Prophet.
       Its ONLY difference from the Quran: a human (Imam al-Bukhari)
       drew the boundaries, not God.

If Quran significant + Bukhari not → the fingerprint is in DIVINE division.

File structure: each line = one hadith (1,000 hadith | 66,349 words)

Tests (same 4-battery as Experiment 08):
  A — Natural hadith units (1,000 hadith — Bukhari's own structure)
  B — Equal division (1,000 × ~66 words)
  C — Random division × 1,000
  D — Bukhari split using Quran's Surah lengths (114 units, direct comparison)

Intellectual property: Emad Suleiman Alwan — March 17, 2026
"""

import sqlite3
import random
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import KHASS_6, digit_root, word_value

random.seed(42)  # Fixed seed for bitwise reproducibility

DB_PATH      = os.environ.get("D369_DB",   "/root/d369/d369.db")
BUKHARI_PATH = os.environ.get("D369_DATA", "/root/d369/data") + "/bukhari_sample.txt"


def load_bukhari(path: str) -> tuple:
    """Each line = one hadith. Returns k6 values + hadith sizes."""
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    all_vals, hadith_sizes = [], []
    for line in lines:
        words = re.findall(r'[\u0600-\u06FF]{2,}', line)
        vals  = [word_value(w, KHASS_6) for w in words]
        all_vals.extend(vals)
        hadith_sizes.append(len(vals))
    return all_vals, hadith_sizes


def load_quran_surah_sizes(db_path: str) -> list:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM words GROUP BY surah_id ORDER BY surah_id")
    sizes = [r[0] for r in c.fetchall()]
    conn.close()
    return sizes


def count_369(vals: list, sizes: list) -> int:
    idx = count = 0
    for sz in sizes:
        if digit_root(sum(vals[idx:idx+sz])) in (3, 6, 9): count += 1
        idx += sz
    return count


def count_369_wrap(vals: list, sizes: list) -> int:
    """Count with cyclic wrap if vals shorter than needed."""
    n = len(vals)
    idx = count = 0
    for sz in sizes:
        chunk = [vals[(idx + i) % n] for i in range(sz)]
        if digit_root(sum(chunk)) in (3, 6, 9): count += 1
        idx = (idx + sz) % n
    return count


def perm_test(vals: list, sizes: list, observed: int, trials: int = 10_000) -> float:
    v = vals.copy(); exceed = 0
    for _ in range(trials):
        random.shuffle(v)
        if count_369(v, sizes) >= observed: exceed += 1
    return exceed / trials


def perm_test_wrap(vals: list, sizes: list, observed: int, trials: int = 5_000) -> float:
    v = vals.copy(); exceed = 0
    for _ in range(trials):
        random.shuffle(v)
        if count_369_wrap(v, sizes) >= observed: exceed += 1
    return exceed / trials


def random_dist(vals: list, n_units: int, trials: int = 1_000) -> list:
    N = len(vals); counts = []
    for _ in range(trials):
        cuts = sorted(random.sample(range(1, N), n_units - 1))
        sizes = ([cuts[0]]
                 + [cuts[i] - cuts[i-1] for i in range(1, n_units - 1)]
                 + [N - cuts[-1]])
        counts.append(count_369(vals, sizes))
    counts.sort()
    return counts


def run(db_path: str = DB_PATH, bukhari_path: str = BUKHARI_PATH) -> dict:
    print("=" * 65)
    print("Experiment 09 — Bukhari as Control Group (Gate Six)")
    print("=" * 65)
    print("\nLogic:")
    print("  Bukhari = Arabic ✓ | Religious ✓ | About the Prophet ✓")
    print("  Only difference from the Quran: a HUMAN drew the boundaries")

    buk_vals, hadith_sizes = load_bukhari(bukhari_path)
    surah_sizes = load_quran_surah_sizes(db_path)
    N = len(buk_vals)
    n_hadith = len(hadith_sizes)

    print(f"\nBukhari: {N:,} words | {n_hadith:,} hadith")
    print(f"Method: each line = 1 hadith | Special-6 values from KHASS_6")

    # Test A — Natural hadith units
    print(f"\n{'─'*55}")
    print(f"Test A — Natural hadith ({n_hadith:,} hadith — Bukhari's own structure)")
    obs_A = count_369(buk_vals, hadith_sizes)
    print(f"   {{3,6,9}} = {obs_A}/{n_hadith} = {obs_A/n_hadith*100:.1f}%  — permutation test (10,000)...")
    p_A = perm_test(buk_vals, hadith_sizes, obs_A, 10_000)
    print(f"   p = {p_A:.4f}  {'✅ significant' if p_A<0.05 else '✗ not significant'}")

    # Test B — Equal division
    print(f"\n{'─'*55}")
    chunk = N // n_hadith
    equal_sizes = [chunk] * (n_hadith - 1) + [N - chunk * (n_hadith - 1)]
    print(f"Test B — Equal division ({n_hadith} × ~{chunk} words)")
    obs_B = count_369(buk_vals, equal_sizes)
    print(f"   {{3,6,9}} = {obs_B}/{n_hadith} = {obs_B/n_hadith*100:.1f}%  — permutation test (5,000)...")
    p_B = perm_test(buk_vals, equal_sizes, obs_B, 5_000)
    print(f"   p = {p_B:.4f}  {'✅ significant' if p_B<0.05 else '✗ not significant'}")

    # Test C — Random × 1,000
    print(f"\n{'─'*55}")
    print(f"Test C — Random division × 1,000 ({n_hadith} units)")
    rand_counts = random_dist(buk_vals, n_hadith, 1_000)
    median_C = rand_counts[500]
    pct_A    = sum(1 for x in rand_counts if x < obs_A) / 10
    thr95    = rand_counts[950]
    print(f"   Median:          {median_C}/{n_hadith} = {median_C/n_hadith*100:.1f}%")
    print(f"   95th percentile: {thr95}/{n_hadith}")
    print(f"   Natural hadith ({obs_A}) at {pct_A:.1f}th percentile — {'exceptional' if pct_A>=95 else 'not exceptional'}")

    # Test D — Bukhari with Quran's Surah lengths
    print(f"\n{'─'*55}")
    print("Test D — Bukhari split using Quran's Surah lengths (114 units)")
    obs_D = count_369_wrap(buk_vals, surah_sizes)
    print(f"   {{3,6,9}} = {obs_D}/114 = {obs_D/114*100:.1f}%  — permutation test (5,000)...")
    p_D = perm_test_wrap(buk_vals, surah_sizes, obs_D, 5_000)
    print(f"   p = {p_D:.4f}  {'✅ significant' if p_D<0.05 else '✗ not significant'}")

    # Summary
    print(f"\n{'='*65}")
    print(f"{'Division':<30} {'Units':>7} {'{{3,6,9}}':>9} {'Pct':>7} {'p-value':>10}")
    print("─" * 65)
    print(f"  {'A: Natural hadith':<28} {n_hadith:>7} {obs_A:>9} {obs_A/n_hadith*100:>6.1f}% {p_A:>10.4f}  {'✅' if p_A<0.05 else '✗'}")
    print(f"  {'B: Equal (~66 words)':<28} {n_hadith:>7} {obs_B:>9} {obs_B/n_hadith*100:>6.1f}% {p_B:>10.4f}  {'✅' if p_B<0.05 else '✗'}")
    print(f"  {'C: Random (median)':<28} {n_hadith:>7} {median_C:>9} {median_C/n_hadith*100:>6.1f}% {'—':>10}  ({obs_A} at {pct_A:.0f}th pct)")
    print(f"  {'D: Quran Surah lengths':<28} {114:>7} {obs_D:>9} {obs_D/114*100:>6.1f}% {p_D:>10.4f}  {'✅' if p_D<0.05 else '✗'}")
    print("=" * 65)

    print(f"\nComparison — Quran vs Bukhari:")
    print(f"  Quran — real Surahs:       51/114 = 44.7%  p=0.007  ✅  (divine division)")
    print(f"  Quran — verses:          2164/6236 = 34.7%  p=0.010  ✅")
    print(f"  Bukhari — natural hadith: {obs_A}/{n_hadith} = {obs_A/n_hadith*100:.1f}%  p={p_A:.3f}  {'✅' if p_A<0.05 else '✗'}  (human division)")

    print("\nVerdict:")
    if p_A >= 0.05 and p_B >= 0.05 and p_D >= 0.05:
        print("→ Bukhari shows no fingerprint under any division")
        print("  The property belongs to the Quran alone")
        print("  The only variable: who drew the boundaries")
    elif p_A < 0.05:
        print("→ Bukhari shows a fingerprint in its natural division")
        print("  The property may extend to human religious texts")
    else:
        print("→ Composite result — requires deeper analysis")

    return {
        "A": {"obs": obs_A, "n": n_hadith, "p": p_A},
        "B": {"obs": obs_B, "n": n_hadith, "p": p_B},
        "C": {"median": median_C, "percentile_A": pct_A, "threshold_95": thr95},
        "D": {"obs": obs_D, "n": 114, "p": p_D},
    }


if __name__ == "__main__":
    run()
