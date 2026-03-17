"""
Experiment 03 — Word-Level Digital Root Fingerprint (5 Texts)
=============================================================
Question: Is the proportion of words with digital root in {3, 6, 9}
          unusually high in the Quran compared to other Arabic texts?

Method:
  1. For each word: compute its Abjad value, then its digital root
  2. Count the fraction with roots in {3, 6, 9}
  3. Chi-Square test: does the distribution differ from uniform (11.1% each)?

Texts tested:
  - The Quran (78,248 words)
  - Sahih al-Bukhari (sample)
  - Sahih Muslim (sample)
  - Ibn Arabi's Futuhat (sample)
  - The Seven Mu'allaqat

Intellectual property: Emad Suleiman Alwan — 2026
"""

import sqlite3
import re
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import JUMMAL_5, digit_root, word_value

DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")
DATA_DIR = os.environ.get("D369_DATA", "/root/d369/data")


def analyze_words_from_db(db_path: str) -> dict:
    """Analyze Quranic words from the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT jummal_value FROM words WHERE jummal_value > 0")
    values = [r[0] for r in c.fetchall()]
    conn.close()

    roots = [digit_root(v) for v in values]
    cnt = Counter(roots)
    n = len(roots)
    count_369 = cnt[3] + cnt[6] + cnt[9]
    return {"n": n, "count_369": count_369, "pct": count_369/n*100, "distribution": dict(cnt)}


def analyze_text_file(path: str, label: str) -> dict:
    """Analyze an external Arabic text file."""
    try:
        with open(path, encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return {"label": label, "error": f"File not found: {path}"}

    words = re.findall(r'[\u0600-\u06FF]{2,}', text)
    roots = [digit_root(word_value(w, JUMMAL_5)) for w in words if word_value(w, JUMMAL_5) > 0]
    if not roots:
        return {"label": label, "error": "No valid words found"}

    cnt = Counter(roots)
    n = len(roots)
    count_369 = cnt[3] + cnt[6] + cnt[9]
    return {"label": label, "n": n, "count_369": count_369, "pct": count_369/n*100, "distribution": dict(cnt)}


def chi_square_test(distribution: dict, n: int) -> tuple:
    """Chi-Square: does the distribution differ from uniform (11.1% each root)?"""
    try:
        from scipy import stats
        observed = [distribution.get(r, 0) for r in range(1, 10)]
        expected = [n / 9] * 9
        chi2, p = stats.chisquare(observed, expected)
        return chi2, p
    except ImportError:
        return None, None


def run(db_path: str = DB_PATH, data_dir: str = DATA_DIR) -> list:
    print("=" * 60)
    print("Experiment 03 — Word-Level Digital Root Fingerprint")
    print("Abjad (ة=5) — 5 texts")
    print("=" * 60)

    results = []

    quran = analyze_words_from_db(db_path)
    quran["label"] = "Quran"
    results.append(quran)

    texts = [
        (os.path.join(data_dir, "bukhari_sample.txt"), "Sahih al-Bukhari"),
        (os.path.join(data_dir, "muslim_sample.txt"), "Sahih Muslim"),
        (os.path.join(data_dir, "futuhat_v1.txt"), "Ibn Arabi — Futuhat"),
        (os.path.join(data_dir, "muallaqat.txt"), "The Seven Mu'allaqat"),
    ]
    for path, label in texts:
        results.append(analyze_text_file(path, label))

    print(f"\n{'Text':>22} | {'Words':>8} | {{3,6,9}} | Pct   | Chi-Sq p")
    print("─" * 70)
    for r in results:
        if "error" in r:
            print(f"  {r['label']:>20} | ⚠️  {r['error']}")
            continue
        chi2, p = chi_square_test(r["distribution"], r["n"])
        p_str = f"{p:.3f}" if p is not None else "N/A"
        star = "✅" if p is not None and p < 0.05 else ""
        print(f"  {r['label']:>20} | {r['n']:>7,} | {r['count_369']:>6} | {r['pct']:>5.1f}%  | {p_str} {star}")

    # Detailed distribution for the Quran
    print(f"\nDigital root distribution — Quran words:")
    dist = results[0].get("distribution", {})
    n = results[0].get("n", 1)
    for r in range(1, 10):
        bar = "█" * int(dist.get(r, 0) / n * 100)
        mark = " ← {3,6,9}" if r in (3, 6, 9) else ""
        print(f"  {r}: {dist.get(r,0):>6} ({dist.get(r,0)/n*100:.1f}%) {bar}{mark}")

    return results


if __name__ == "__main__":
    run()
