"""
Experiment 27 — Letter-Frequency Null Model (Vectorized)
========================================================

Date: April 13, 2026

See NOTES.md for full rationale.

Fast implementation using numpy segment-sum so 1000 Monte Carlo trials
× 78,248 words run in under a minute.
"""

import sqlite3
import json
import os
from collections import Counter
import numpy as np

np.random.seed(369)

DB = "/home/emad/d369-quran-fingerprint/data/d369_research.db"
BUKHARI_TXT = "/home/emad/d369-quran-fingerprint/data/bukhari_sample.txt"
RESULTS = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS, exist_ok=True)

# Standard Abjad, with common hamza/ta-marbuta forms mapped to canonical
ABJAD = {
    'ا':1, 'ب':2, 'ج':3, 'د':4, 'ه':5, 'و':6, 'ز':7, 'ح':8, 'ط':9,
    'ي':10, 'ك':20, 'ل':30, 'م':40, 'ن':50, 'س':60, 'ع':70, 'ف':80, 'ص':90,
    'ق':100, 'ر':200, 'ش':300, 'ت':400, 'ث':500, 'خ':600, 'ذ':700, 'ض':800,
    'ظ':900, 'غ':1000,
    'أ':1, 'إ':1, 'آ':1, 'ء':1, 'ئ':1, 'ؤ':1,
    'ة':5, 'ى':10,
}


def load_quran():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT text_clean, jummal_value FROM words").fetchall()
    conn.close()
    return rows


def letter_counter(words):
    c = Counter()
    for w, _ in words:
        for ch in w:
            if ch in ABJAD:
                c[ch] += 1
    return c


def length_distribution(words):
    c = Counter()
    for w, _ in words:
        ln = sum(1 for ch in w if ch in ABJAD)
        if ln > 0:
            c[ln] += 1
    return c


def load_bukhari_letters():
    with open(BUKHARI_TXT, encoding='utf-8') as f:
        text = f.read()
    c = Counter()
    for ch in text:
        if ch in ABJAD:
            c[ch] += 1
    return c


def quran_actual_pct(words):
    """Compute %{3,6,9} on the real Quran words."""
    vals = np.array([v for _, v in words if v > 0])
    # digital root: 1+((n-1)%9)
    drs = 1 + (vals - 1) % 9
    in369 = np.isin(drs, [3, 6, 9])
    return 100.0 * in369.mean(), len(vals)


def monte_carlo_null_fast(letter_counts: Counter, length_counts: Counter,
                          n_words: int, n_trials: int = 1000) -> dict:
    """
    Vectorized null generator.

    For each trial:
      1. Sample n_words word lengths.
      2. Compute total letters needed; sample that many letter values in one go.
      3. Use np.add.reduceat to sum letters into words.
      4. Compute DR vectorized; count in {3,6,9}.
    """
    letters = list(letter_counts.keys())
    letter_vals = np.array([ABJAD[l] for l in letters], dtype=np.int64)
    l_probs = np.array([letter_counts[l] for l in letters], dtype=float)
    l_probs /= l_probs.sum()

    lengths_keys = np.array(list(length_counts.keys()), dtype=np.int64)
    len_probs = np.array([length_counts[l] for l in length_counts.keys()], dtype=float)
    len_probs /= len_probs.sum()

    pcts = np.empty(n_trials)
    for t in range(n_trials):
        sampled_lens = np.random.choice(lengths_keys, size=n_words, p=len_probs)
        total_letters = int(sampled_lens.sum())
        idx = np.random.choice(len(letters), size=total_letters, p=l_probs)
        vals_flat = letter_vals[idx]
        # reduceat needs start positions
        starts = np.concatenate(([0], np.cumsum(sampled_lens[:-1])))
        word_sums = np.add.reduceat(vals_flat, starts)
        # filter nonzero (should be none; min length≥1 ensures >0)
        mask = word_sums > 0
        drs = 1 + (word_sums[mask] - 1) % 9
        pct = 100.0 * np.isin(drs, [3, 6, 9]).mean()
        pcts[t] = pct

    return {
        "n_trials": n_trials,
        "n_words_per_trial": n_words,
        "mean_pct_369": float(pcts.mean()),
        "std": float(pcts.std()),
        "ci95_low": float(np.percentile(pcts, 2.5)),
        "ci95_high": float(np.percentile(pcts, 97.5)),
        "min": float(pcts.min()),
        "max": float(pcts.max()),
    }


def residue_diagnostic(name: str, ctr: Counter):
    total = sum(ctr.values())
    r = {0: 0, 1: 0, 2: 0}
    for l, c in ctr.items():
        r[ABJAD[l] % 3] += c
    print(f"  {name:<15} n={total:>8}  "
          f"r≡0: {100*r[0]/total:5.2f}%   "
          f"r≡1: {100*r[1]/total:5.2f}%   "
          f"r≡2: {100*r[2]/total:5.2f}%")


def main():
    print("=" * 72)
    print("Experiment 27 — Letter-Frequency Null Model (vectorized)")
    print("=" * 72)

    words = load_quran()
    quran_pct, n_quran = quran_actual_pct(words)
    quran_letters = letter_counter(words)
    quran_lengths = length_distribution(words)
    bukhari_letters = load_bukhari_letters()
    uniform_letters = Counter({ch: 1 for ch in 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'})

    print(f"\nQuran observed: n={n_quran}  %{{3,6,9}} = {quran_pct:.2f}%\n")
    print("Letter residue mod 3 diagnostic (predicts null mean):")
    residue_diagnostic("Quran",   quran_letters)
    residue_diagnostic("Bukhari", bukhari_letters)
    residue_diagnostic("Uniform", uniform_letters)

    n_trials = 1000
    print(f"\nMonte Carlo: {n_trials} trials × {n_quran} words per trial")

    scenarios = [
        ("null_quran_letters",    quran_letters),
        ("null_bukhari_letters",  bukhari_letters),
        ("null_uniform_letters",  uniform_letters),
    ]

    all_results = {"quran_observed": {"pct_369": round(quran_pct, 4), "n": n_quran}}

    for name, lctr in scenarios:
        r = monte_carlo_null_fast(lctr, quran_lengths, n_quran, n_trials)
        all_results[name] = r
        gap = quran_pct - r["mean_pct_369"]
        inside = r["ci95_low"] <= quran_pct <= r["ci95_high"]
        verdict = "INSIDE 95% CI — confounded" if inside else "OUTSIDE 95% CI — signal"
        print(f"\n{name}")
        print(f"  null mean: {r['mean_pct_369']:.2f}%  std: {r['std']:.3f}  "
              f"95%CI: [{r['ci95_low']:.2f}, {r['ci95_high']:.2f}]")
        print(f"  Quran obs: {quran_pct:.2f}%   gap: +{gap:.2f} pp   {verdict}")

    path = os.path.join(RESULTS, "results.json")
    with open(path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved: {path}")

    print("\n" + "=" * 72)
    print("FINAL TABLE")
    print("=" * 72)
    print(f"{'Model':<30} {'%{3,6,9}':<12} {'vs Quran':<10}")
    print("-" * 72)
    print(f"{'Uniform baseline (theoretical)':<30} {33.33:<12.2f} {quran_pct-33.33:+.2f}")
    for name, _ in scenarios:
        m = all_results[name]["mean_pct_369"]
        print(f"{name:<30} {m:<12.2f} {quran_pct-m:+.2f}")
    print(f"{'QURAN observed':<30} {quran_pct:<12.2f} {'—':<10}")


if __name__ == "__main__":
    main()
