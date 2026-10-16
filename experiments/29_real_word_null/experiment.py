"""
Experiment 29 — Real-Arabic-Word Null
=====================================

Date: April 13, 2026
Priority: CRITICAL — strongest remaining empirical attack vector.

PURPOSE
-------
Exp 27 used a Monte Carlo null drawing INDEPENDENT random letters.
A reviewer will object: "Arabic words are not random letter sequences —
they follow triliteral root morphology, phonotactic constraints, and
semantic distributions. Your 41% null is unrealistic. Use REAL Arabic
words, sampled to match Quran's length distribution."

This experiment implements that demand. We sample actual Bukhari
(and Muslim hadith + Futuhat + Muallaqat) words matched by length
to the Quran, and measure the composite %{3,6,9} rate.

If null ≈ 45% → Quran's 48.44% advantage shrinks to ~3 pp (weak signal)
If null ≈ 42% → Quran's advantage is ~6 pp (real signal)
If null ≈ 38% → Quran's advantage is ~10 pp (strong signal)

METHODOLOGY
-----------
1. Load full word lists (with Abjad values) from:
   - Bukhari sample      (hadith)
   - Muslim sample       (hadith)
   - Futuhat (Ibn Arabi) (Sufi prose)
   - Muallaqat           (pre-Islamic poetry)

2. For each source corpus C and each of 500 Monte Carlo trials:
   - Sample n=78,248 words from C WITH REPLACEMENT, where each sample
     is drawn from the pool of C-words of the SAME length ℓ, and ℓ
     itself is drawn from the Quranic length distribution.
   - Compute composite-only %{3,6,9}.

3. Report mean, 95% CI per corpus. Compare to Quran 48.44%.

This is an "empirical null" — it assumes natural Arabic provides the
correct baseline for what a non-divine Arabic text looks like.

Intellectual property: Emad Suleiman Alwan — up2b.ai — 2026
"""

import sqlite3
import json
import os
import re
from collections import Counter, defaultdict
import numpy as np
from sympy import isprime

np.random.seed(369)

DATA = "/home/emad/d369-quran-fingerprint/data"
DB = os.path.join(DATA, "d369_research.db")
RESULTS = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS, exist_ok=True)

ABJAD = {
    'ا':1,'ب':2,'ج':3,'د':4,'ه':5,'و':6,'ز':7,'ح':8,'ط':9,
    'ي':10,'ك':20,'ل':30,'م':40,'ن':50,'س':60,'ع':70,'ف':80,'ص':90,
    'ق':100,'ر':200,'ش':300,'ت':400,'ث':500,'خ':600,'ذ':700,'ض':800,
    'ظ':900,'غ':1000,
    'أ':1,'إ':1,'آ':1,'ء':1,'ئ':1,'ؤ':1,'ة':5,'ى':10
}


def dr(n):
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def abjad_value(word):
    return sum(ABJAD[ch] for ch in word if ch in ABJAD)


def tokenize_arabic_corpus(path):
    """Extract Arabic words from a text file, return list of (word, abjad_value)."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    # Split on non-Arabic-letter characters
    tokens = re.findall(r'[\u0600-\u06FF]+', text)
    out = []
    for t in tokens:
        # Keep only chars we can map
        clean = ''.join(c for c in t if c in ABJAD)
        if clean:
            v = abjad_value(clean)
            if v > 0:
                out.append((clean, v))
    return out


def group_by_length(words):
    """Return {length: [abjad_values]}."""
    g = defaultdict(list)
    for w, v in words:
        ln = sum(1 for c in w if c in ABJAD)
        if ln > 0:
            g[ln].append(v)
    return {k: np.array(v) for k, v in g.items()}


def quran_length_dist():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT text_clean FROM words").fetchall()
    conn.close()
    c = Counter()
    for (w,) in rows:
        ln = sum(1 for ch in w if ch in ABJAD)
        if ln > 0:
            c[ln] += 1
    return c


def quran_observed_composite_pct():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT jummal_value FROM words").fetchall()
    conn.close()
    vals = [v for (v,) in rows if v > 0]
    comp = [v for v in vals if not isprime(v)]
    drs = [dr(v) for v in comp]
    n369 = sum(1 for d in drs if d in {3,6,9})
    return 100 * n369 / len(drs), len(comp)


def null_from_corpus(corpus_words_by_len, length_dist, n_target=78248,
                     n_trials=500, label=""):
    """For each trial: sample n_target words with Quran-length distribution,
       drawn from the given corpus pool (by length). Compute composite %369."""
    lens_keys = np.array(list(length_dist.keys()))
    len_probs = np.array([length_dist[k] for k in lens_keys], dtype=float)
    len_probs /= len_probs.sum()

    # Filter: only use lengths that exist in the corpus
    available_lens = set(corpus_words_by_len.keys())
    mask = [k in available_lens for k in lens_keys]
    lens_keys = lens_keys[mask]
    len_probs = len_probs[mask]
    len_probs /= len_probs.sum()

    pcts = []
    for t in range(n_trials):
        # Sample which lengths to draw
        sampled_lens = np.random.choice(lens_keys, size=n_target, p=len_probs)
        len_counts = Counter(sampled_lens.tolist())
        # For each length, draw that many words from the corpus pool of that length
        all_vals = []
        for ln, cnt in len_counts.items():
            pool = corpus_words_by_len[ln]
            drawn = np.random.choice(pool, size=cnt, replace=True)
            all_vals.append(drawn)
        all_vals = np.concatenate(all_vals)
        # Composite-only (primality test — expensive but correct)
        comp_mask = np.array([not isprime(int(v)) for v in all_vals])
        comp_vals = all_vals[comp_mask]
        drs = 1 + (comp_vals - 1) % 9
        pct = 100 * np.isin(drs, [3,6,9]).mean()
        pcts.append(pct)
        if (t+1) % 50 == 0:
            print(f"  {label}: trial {t+1}/{n_trials} done, running mean = "
                  f"{np.mean(pcts):.2f}%")
    pcts = np.array(pcts)
    return {
        "n_trials": n_trials,
        "mean_pct_369": float(pcts.mean()),
        "std": float(pcts.std()),
        "ci95_low": float(np.percentile(pcts, 2.5)),
        "ci95_high": float(np.percentile(pcts, 97.5)),
        "min": float(pcts.min()),
        "max": float(pcts.max()),
    }


def main(n_trials=300):
    print("=" * 72)
    print("Experiment 29 — Real-Arabic-Word Null")
    print("=" * 72)

    quran_pct, n_quran_comp = quran_observed_composite_pct()
    print(f"\nQuran composite observed: {quran_pct:.2f}% ({n_quran_comp} words)")

    length_dist = quran_length_dist()

    sources = {
        "bukhari":   os.path.join(DATA, "bukhari_sample.txt"),
        "muallaqat": os.path.join(DATA, "muallaqat.txt"),
        "futuhat":   os.path.join(DATA, "futuhat_v1.txt"),
    }
    # Add Muslim if available
    muslim_p = "/home/emad/d369/data/muslim_sample.txt"
    if os.path.exists(muslim_p):
        sources["muslim"] = muslim_p

    results = {"quran_observed": {"pct_369_composite": quran_pct,
                                   "n_composite": n_quran_comp}}

    for name, path in sources.items():
        if not os.path.exists(path):
            print(f"\n[skip] {name}: file not found")
            continue
        print(f"\n{'-'*72}")
        print(f"Corpus: {name}  — loading from {path}")
        words = tokenize_arabic_corpus(path)
        pool_by_len = group_by_length(words)
        print(f"  total words: {len(words)}")
        print(f"  distinct lengths: {sorted(pool_by_len.keys())[:10]}...")
        # Compute corpus's own baseline composite %369 (for context)
        comp_all = [v for _, v in words if not isprime(v)]
        own_pct = 100 * sum(1 for v in comp_all if dr(v) in {3,6,9}) / len(comp_all)
        print(f"  own composite %{{3,6,9}} = {own_pct:.2f}%")

        r = null_from_corpus(pool_by_len, length_dist, 78248, n_trials, label=name)
        r["own_composite_pct"] = own_pct
        r["n_words"] = len(words)
        gap = quran_pct - r["mean_pct_369"]
        r["gap_vs_quran"] = gap
        outside = quran_pct > r["ci95_high"] or quran_pct < r["ci95_low"]
        r["quran_outside_ci"] = bool(outside)
        results[f"null_{name}"] = r
        print(f"\n  RESULT: null mean={r['mean_pct_369']:.2f}%  "
              f"95%CI=[{r['ci95_low']:.2f}, {r['ci95_high']:.2f}]")
        print(f"  Quran gap: +{gap:.2f} pp  "
              f"{'✓ OUTSIDE CI (signal)' if outside else '✗ inside CI (confounded)'}")

    # Save
    with open(os.path.join(RESULTS, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 72)
    print("FINAL SUMMARY — Real-Arabic-Word Nulls")
    print("=" * 72)
    print(f"{'Source':<15} {'Null %369':<12} {'95% CI':<25} {'Gap':<10} {'Signal?'}")
    print("-" * 72)
    for key, r in results.items():
        if key == "quran_observed": continue
        name = key.replace("null_", "")
        ci = f"[{r['ci95_low']:.2f}, {r['ci95_high']:.2f}]"
        sig = "✓" if r["quran_outside_ci"] else "✗"
        print(f"{name:<15} {r['mean_pct_369']:<12.2f} {ci:<25} "
              f"+{r['gap_vs_quran']:<9.2f} {sig}")
    print(f"{'QURAN observed':<15} {quran_pct:<12.2f}")


if __name__ == "__main__":
    main(n_trials=300)
