"""
Experiment 04 — Special-6 at the Surah Level (The Decisive Test)
================================================================
Question: Does the Special-6 encoding (a quasi-binary system, independent
          of Abjad) reveal the {3, 6, 9} fingerprint in 114 Surahs?
          And is this fingerprint unique to the Quran?

Special-6 is completely independent of Abjad:
  - Abjad: 28 phonemes (ا=أ=إ=آ=1)
  - Special-6: 33 letter shapes (ة≠ت, ؤ≠و, ئ≠ي)

Method:
  1. Load Special-6 values per word from the database
  2. Sum per Surah, compute digital root
  3. Count Surahs with root in {3, 6, 9}
  4. Permutation test (10,000 trials): shuffle word values across Surahs
  5. Repeat for 3 control texts (Bukhari, Ibn Arabi, Mu'allaqat)

Key finding: p = 0.007 for the Quran | p > 0.38 for all other texts

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


def load_quran_k6(db_path: str) -> tuple:
    """
    Load Special-6 values for every word, with their Surah IDs.
    Returns: (list of k6 values, list of Surah sizes in order)
    """
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

    surah_ids = [r[0] for r in rows]
    k6_values = [r[1] for r in rows]

    sizes = defaultdict(int)
    for sid in surah_ids:
        sizes[sid] += 1

    return k6_values, [sizes[s] for s in sorted(sizes)]


def count_369(values: list, sizes: list) -> int:
    """Count Surahs whose Special-6 sum has a digital root in {3, 6, 9}."""
    idx = 0
    count = 0
    for sz in sizes:
        total = sum(values[idx:idx+sz])
        if digit_root(total) in (3, 6, 9):
            count += 1
        idx += sz
    return count


def permutation_test(values: list, sizes: list, observed: int, trials: int = 10_000) -> float:
    """
    Permutation test: shuffle word values randomly across Surah boundaries,
    count how often the shuffled arrangement achieves >= observed {3,6,9} count.
    This is the correct null model (preserves the actual word value distribution).
    """
    vc = values.copy()
    exceed = 0
    for _ in range(trials):
        random.shuffle(vc)
        if count_369(vc, sizes) >= observed:
            exceed += 1
    return exceed / trials


def test_text_file(path: str, label: str, n_chunks: int = 114, trials: int = 2_000) -> dict:
    """Test an external text by splitting it into n_chunks and applying the same test."""
    try:
        with open(path, encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return {"label": label, "error": "File not found"}

    words = re.findall(r'[\u0600-\u06FF]{2,}', text)
    if len(words) < n_chunks * 10:
        n_chunks = max(10, len(words) // 50)

    k6_vals = [word_value(w, KHASS_6) for w in words]
    sz = len(k6_vals) // n_chunks
    sizes = [sz] * (n_chunks - 1) + [len(k6_vals) - sz * (n_chunks - 1)]

    obs = count_369(k6_vals, sizes)
    p = permutation_test(k6_vals, sizes, obs, trials)

    return {
        "label": label,
        "n_words": len(words),
        "n_chunks": n_chunks,
        "observed": obs,
        "pct": obs / n_chunks * 100,
        "p_value": p
    }


def run(db_path: str = DB_PATH, data_dir: str = DATA_DIR,
        perm_trials: int = 10_000) -> dict:
    print("=" * 60)
    print("Experiment 04 — Special-6 at Surah Level")
    print("The decisive test: is the fingerprint unique to the Quran?")
    print("=" * 60)

    # Quran
    print("\nLoading Quran data...")
    k6_values, sizes = load_quran_k6(db_path)
    obs_quran = count_369(k6_values, sizes)
    n_surahs = len(sizes)

    print(f"Quran: {sum(sizes):,} words | {n_surahs} Surahs")
    print(f"  {{3,6,9}} = {obs_quran}/{n_surahs} = {obs_quran/n_surahs*100:.1f}%")
    print(f"  Running permutation test ({perm_trials:,} trials)...")

    p_quran = permutation_test(k6_values, sizes, obs_quran, perm_trials)
    print(f"  p = {p_quran:.5f}  {'✅ significant (p<0.05)' if p_quran < 0.05 else '✗ not significant'}")

    # Control texts
    comparisons = [
        (os.path.join(data_dir, "bukhari_sample.txt"), "Sahih al-Bukhari", 114),
        (os.path.join(data_dir, "futuhat_v1.txt"), "Ibn Arabi — Futuhat", 114),
        (os.path.join(data_dir, "muallaqat.txt"), "The Seven Mu'allaqat", 20),
    ]

    print(f"\n{'─'*55}")
    print("Comparison with other Arabic texts (2,000 trials each):")
    print(f"{'─'*55}")

    comparison_results = []
    for path, label, chunks in comparisons:
        r = test_text_file(path, label, chunks, 2_000)
        if "error" in r:
            print(f"  {label}: ⚠️  {r['error']}")
        else:
            print(f"  {label}: {r['observed']}/{r['n_chunks']} = {r['pct']:.1f}%  |  p = {r['p_value']:.4f}  {'✅' if r['p_value']<0.05 else '✗'}")
        comparison_results.append(r)

    # Summary
    print(f"\n{'='*55}")
    print("Summary")
    print(f"{'='*55}")
    print(f"{'Text':>24} | {{3,6,9}}         | p-value | Verdict")
    print("─" * 60)
    print(f"  {'Quran':>22} | {obs_quran}/{n_surahs}={obs_quran/n_surahs*100:.1f}% | {p_quran:.4f}  | {'✅ significant' if p_quran<0.05 else '✗'}")
    for r in comparison_results:
        if "error" not in r:
            pct_str = f"{r['observed']}/{r['n_chunks']}={r['pct']:.1f}%"
            print(f"  {r['label']:>22} | {pct_str:>15} | {r['p_value']:.4f}  | {'✅' if r['p_value']<0.05 else '✗'}")

    return {
        "quran": {"observed": obs_quran, "n_surahs": n_surahs, "p_value": p_quran},
        "comparisons": comparison_results
    }


if __name__ == "__main__":
    run()
