"""
Experiment 07 — Architecture vs. Words?
========================================
The fundamental question: Is the {3,6,9} fingerprint in the words of
the Quran — or in how they were divided into 114 Surahs of specific lengths?

This question defines the nature of the phenomenon:
  - If fingerprint is in the WORDS → it lives in the linguistic content
  - If fingerprint is in the DIVISION → the 114-Surah architecture is the structure

Method: Three parallel tests using Special-6 encoding

  Test A — Reference:
    Content:  Quran words in their original order
    Division: Original Surah lengths

  Test B — Shuffled words:
    Content:  Quran words shuffled randomly
    Division: Same Surah lengths

  Test C — Foreign text:
    Content:  Sahih al-Bukhari words
    Division: Same Surah lengths (Quran's architecture applied to another text)

Logic:
  A significant ✅ + B not significant ✗ + C not significant ✗
    → fingerprint is in the original WORD ORDER

  A significant ✅ + B significant ✅ + C not significant ✗
    → fingerprint is in the Quranic WORDS regardless of order

  A significant ✅ + B significant ✅ + C significant ✅
    → fingerprint is in the ARCHITECTURE (the 114-Surah division itself)

Results:
  A: 51/114 = 44.7%  p = 0.0093  ✅
  B: 43/114 = 37.7%  p = 0.1853  ✗
  C: 39/114 = 34.2%  p = 0.4497  ✗

Conclusion: The fingerprint is in the words IN THEIR ORIGINAL ORDER.
Neither the words alone nor the architecture alone is sufficient.

Intellectual property: Emad Suleiman Alwan — March 17, 2026
"""

import sqlite3
import re
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import KHASS_6, digit_root, word_value

DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")
DATA_DIR = os.environ.get("D369_DATA", "/root/d369/data")


def get_surah_sizes(db_path: str) -> list:
    """Get word counts per Surah (the Quran's architectural division)."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT surah_id, COUNT(*) as word_count
        FROM words GROUP BY surah_id ORDER BY surah_id
    """)
    sizes = [row[1] for row in c.fetchall()]
    conn.close()
    return sizes


def get_quran_k6(db_path: str) -> list:
    """Get Special-6 values for all Quran words in original order."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT CAST(jummal_special_6 AS INTEGER)
        FROM words ORDER BY word_pos_in_quran
    """)
    vals = [r[0] for r in c.fetchall()]
    conn.close()
    return vals


def get_text_k6(path: str) -> list:
    """Get Special-6 values for words in an external text file."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    words = re.findall(r'[\u0600-\u06FF]{2,}', text)
    return [word_value(w, KHASS_6) for w in words]


def count_369_with_sizes(values: list, sizes: list) -> tuple:
    """
    Count {3,6,9} digital roots across Surah-sized chunks.
    If values list is shorter than total needed, wrap around cyclically.
    """
    idx = 0
    count = 0
    details = []
    n = len(values)
    for sz in sizes:
        chunk = [values[(idx + i) % n] for i in range(sz)]
        total = sum(chunk)
        dr = digit_root(total)
        if dr in (3, 6, 9):
            count += 1
        details.append(dr)
        idx = (idx + sz) % n
    return count, details


def permutation_test(values: list, sizes: list, observed: int, trials: int = 3000) -> float:
    """Permutation test: how often does a random shuffle achieve >= observed?"""
    vc = values.copy()
    exceed = 0
    for _ in range(trials):
        random.shuffle(vc)
        cnt, _ = count_369_with_sizes(vc, sizes)
        if cnt >= observed:
            exceed += 1
    return exceed / trials


def run(db_path: str = DB_PATH, data_dir: str = DATA_DIR) -> dict:
    print("=" * 65)
    print("Experiment 07 — Architecture vs. Words?")
    print("Is the fingerprint in the division into 114 Surahs — or in the words?")
    print("=" * 65)

    sizes = get_surah_sizes(db_path)
    n_surahs = len(sizes)
    print(f"\nSurah architecture: {n_surahs} Surahs | total {sum(sizes):,} words")
    print(f"  Shortest: {min(sizes)} words (al-Kawthar) | Longest: {max(sizes)} words (al-Baqara)")

    # Test A — Quran in original order
    print(f"\n{'─'*55}")
    print("Test A — Quran in its original order (reference)")
    quran_vals = get_quran_k6(db_path)
    obs_quran, _ = count_369_with_sizes(quran_vals, sizes)
    p_quran = permutation_test(quran_vals, sizes, obs_quran, 3000)
    print(f"   {{3,6,9}} = {obs_quran}/{n_surahs} = {obs_quran/n_surahs*100:.1f}%  |  p = {p_quran:.4f}  {'✅ significant' if p_quran<0.05 else '✗'}")

    # Test B — Quran words shuffled
    print(f"\n{'─'*55}")
    print("Test B — Quran words shuffled randomly, same Surah sizes")
    shuffled_quran = quran_vals.copy()
    random.shuffle(shuffled_quran)
    obs_shuffled, _ = count_369_with_sizes(shuffled_quran, sizes)
    p_shuffled = permutation_test(shuffled_quran, sizes, obs_shuffled, 3000)
    print(f"   {{3,6,9}} = {obs_shuffled}/{n_surahs} = {obs_shuffled/n_surahs*100:.1f}%  |  p = {p_shuffled:.4f}  {'✅ significant' if p_shuffled<0.05 else '✗'}")

    # Test C — Bukhari with Quran's Surah lengths
    bukhari_path = os.path.join(data_dir, "bukhari_sample.txt")
    print(f"\n{'─'*55}")
    print("Test C — Bukhari split using Quran's Surah lengths")
    try:
        bukhari_vals = get_text_k6(bukhari_path)
        print(f"   Bukhari: {len(bukhari_vals):,} words")
        obs_bukhari, _ = count_369_with_sizes(bukhari_vals, sizes)
        p_bukhari = permutation_test(bukhari_vals, sizes, obs_bukhari, 3000)
        print(f"   {{3,6,9}} = {obs_bukhari}/{n_surahs} = {obs_bukhari/n_surahs*100:.1f}%  |  p = {p_bukhari:.4f}  {'✅ significant' if p_bukhari<0.05 else '✗'}")
    except FileNotFoundError:
        print("   ⚠️  Bukhari file not found")
        p_bukhari = None

    # Verdict
    print(f"\n{'='*55}")
    print("Verdict")
    print(f"{'='*55}")
    print(f"  Quran (original order):       p = {p_quran:.4f}  {'✅ significant' if p_quran<0.05 else '✗'}")
    print(f"  Quran (shuffled):             p = {p_shuffled:.4f}  {'✅ significant' if p_shuffled<0.05 else '✗'}")
    if p_bukhari is not None:
        print(f"  Bukhari (Quran architecture): p = {p_bukhari:.4f}  {'✅ significant' if p_bukhari<0.05 else '✗'}")

    print()
    if p_quran < 0.05 and p_shuffled >= 0.05 and (p_bukhari is None or p_bukhari >= 0.05):
        print("→ Fingerprint is in the ORIGINAL WORD ORDER — not merely in the division")
        print("  The words carry the fingerprint in the order they were revealed")
    elif p_quran < 0.05 and p_bukhari is not None and p_bukhari < 0.05:
        print("→ Fingerprint is in the ARCHITECTURE (the 114-Surah division)")
        print("  Any text split by these lengths produces the same result")
    else:
        print("→ Result is composite — requires deeper analysis")

    return {
        "quran_original": {"obs": obs_quran, "p": p_quran},
        "quran_shuffled": {"obs": obs_shuffled, "p": p_shuffled},
        "bukhari_quran_sizes": {"p": p_bukhari}
    }


if __name__ == "__main__":
    run()
