"""
Experiment 32 — Torah (Hebrew) with Full 84-Subset Scan
=======================================================

Date: April 13, 2026
Concept: Emad (cross-language robustness test)

QUESTION
--------
Does the {3,6,9} excess appear in the Hebrew Torah analyzed with
Gematria? Three possible outcomes:

  (a) Torah also shows strong {3,6,9} excess above Hebrew null.
      → Phenomenon extends to revealed texts generally, not Quran alone.

  (b) Torah shows NO excess or weak excess above Hebrew null.
      → Phenomenon is Quran-specific in ways that don't transfer.

  (c) Torah shows a DIFFERENT subset as its top-ranked gap.
      → Phenomenon is language-specific but structured differently
         in different sacred traditions.

Any outcome is scientifically valuable. (a) weakens Quran uniqueness
but strengthens "sacred text signature"; (b) sharpens Quran uniqueness;
(c) opens a comparative-religion-in-numbers research program.

METHODOLOGY
-----------
1. Load Torah (Hebrew) from torah_hebrew.jsonl — 69,196 words.
2. Apply standard Gematria (Mispar Hechrachi): א=1, ב=2, ..., ת=400.
   Final (sofit) letter forms → same value as base form.
3. Compute Abjad-equivalent: each word's gematria value = sum of letter values.
4. Compute digital root distribution (all words + composite only).
5. Run full 84-subset scan (same as Exp 30) with Hebrew-letter
   frequency Monte Carlo null.
6. Identify:
     - Where does {3,6,9} rank in Torah?
     - What is Torah's top subset?
     - Is it closed under addition/multiplication (like Quran's was)?

Intellectual property: Emad Suleiman Alwan — up2b.ai — 2026
"""

import json
import os
from itertools import combinations
from collections import Counter, defaultdict
import numpy as np
from sympy import isprime

np.random.seed(369)

TORAH_PATH = "/home/emad/d369/data/torah_hebrew.jsonl"
RESULTS = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS, exist_ok=True)

# Standard Hebrew Gematria (Mispar Hechrachi)
GEMATRIA = {
    'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,
    'י':10,'כ':20,'ל':30,'מ':40,'נ':50,'ס':60,'ע':70,'פ':80,'צ':90,
    'ק':100,'ר':200,'ש':300,'ת':400,
    # Sofit (final) forms → same as base
    'ך':20, 'ם':40, 'ן':50, 'ף':80, 'ץ':90,
}


def dr(n):
    if n == 0: return 0
    r = n % 9
    return 9 if r == 0 else r


def gematria(word):
    return sum(GEMATRIA[ch] for ch in word if ch in GEMATRIA)


def load_torah():
    words = []
    with open(TORAH_PATH, encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            for w in verse['words']:
                clean = ''.join(c for c in w if c in GEMATRIA)
                if clean:
                    v = gematria(clean)
                    if v > 0:
                        words.append((clean, v))
    return words


def group_by_length(words):
    g = defaultdict(list)
    for w, v in words:
        ln = sum(1 for c in w if c in GEMATRIA)
        if ln > 0:
            g[ln].append(v)
    return {k: np.array(v) for k, v in g.items()}


def letter_frequency(words):
    c = Counter()
    for w, _ in words:
        for ch in w:
            if ch in GEMATRIA:
                c[ch] += 1
    return c


def length_distribution(words):
    c = Counter()
    for w, _ in words:
        ln = sum(1 for ch in w if ch in GEMATRIA)
        if ln > 0:
            c[ln] += 1
    return c


def closure_properties():
    """Compute which size-3 subsets of {1..9} are closed under +/×."""
    props = {}
    for combo in combinations(range(1,10), 3):
        S = set(combo)
        add_c = all(dr(a+b) in S for a in combo for b in combo)
        mul_c = all(dr(a*b) in S for a in combo for b in combo)
        props[combo] = {"add": add_c, "mul": mul_c, "both": add_c and mul_c}
    return props


def monte_carlo_dr_dist(letter_counts, length_counts, n_target, n_trials):
    """Generate synthetic words via letter-frequency MC, return per-trial
       DR distribution (composite-only) as (n_trials, 9) array."""
    letters = list(letter_counts.keys())
    letter_vals = np.array([GEMATRIA[l] for l in letters], dtype=np.int64)
    l_probs = np.array([letter_counts[l] for l in letters], dtype=float)
    l_probs /= l_probs.sum()

    lens_keys = np.array(list(length_counts.keys()))
    len_probs = np.array([length_counts[k] for k in lens_keys], dtype=float)
    len_probs /= len_probs.sum()

    trial_dr = np.zeros((n_trials, 9))
    for t in range(n_trials):
        sampled_lens = np.random.choice(lens_keys, size=n_target, p=len_probs)
        total = int(sampled_lens.sum())
        idx = np.random.choice(len(letters), size=total, p=l_probs)
        flat = letter_vals[idx]
        starts = np.concatenate(([0], np.cumsum(sampled_lens[:-1])))
        sums = np.add.reduceat(flat, starts)
        sums = sums[sums > 0]
        # composite only
        comp_mask = np.array([not isprime(int(s)) for s in sums])
        comp = sums[comp_mask]
        drs = 1 + (comp - 1) % 9
        bc = np.bincount(drs, minlength=10)[1:10]
        trial_dr[t] = bc / len(comp) * 100
        if (t+1) % 50 == 0:
            print(f"  trial {t+1}/{n_trials}")
    return trial_dr


def main(n_trials=300):
    print("=" * 72)
    print("Experiment 32 — Torah Hebrew + 84-Subset Scan")
    print("=" * 72)

    words = load_torah()
    print(f"\nLoaded Torah: {len(words)} Hebrew words")

    # Torah observed DR distribution (composite only)
    vals = np.array([v for _, v in words])
    comp_mask = np.array([not isprime(int(v)) for v in vals])
    comp = vals[comp_mask]
    drs = 1 + (comp - 1) % 9
    torah_dr_pct = np.bincount(drs, minlength=10)[1:10] / len(comp) * 100
    print(f"\nTorah composite: {len(comp)} words")
    print(f"  DR distribution (composite %): "
          f"{dict(zip(range(1,10), np.round(torah_dr_pct, 2)))}")
    torah_369 = torah_dr_pct[2] + torah_dr_pct[5] + torah_dr_pct[8]
    print(f"  Torah composite %{{3,6,9}} = {torah_369:.2f}%")

    # Hebrew letter residue-mod-3 diagnostic
    letter_cnt = letter_frequency(words)
    total = sum(letter_cnt.values())
    r0 = r1 = r2 = 0
    for l, c in letter_cnt.items():
        res = GEMATRIA[l] % 3
        if res == 0: r0 += c
        elif res == 1: r1 += c
        else: r2 += c
    print(f"\nHebrew letter residue mod 3: r≡0 {100*r0/total:.2f}%   "
          f"r≡1 {100*r1/total:.2f}%   r≡2 {100*r2/total:.2f}%")

    # Length distribution
    len_dist = length_distribution(words)

    # Null Monte Carlo
    print(f"\nRunning null Monte Carlo ({n_trials} trials)...")
    null_dr = monte_carlo_dr_dist(letter_cnt, len_dist, len(words), n_trials)
    null_mean = null_dr.mean(axis=0)
    null_ci_lo = np.percentile(null_dr, 2.5, axis=0)
    null_ci_hi = np.percentile(null_dr, 97.5, axis=0)
    print(f"  Null DR distribution (mean): "
          f"{dict(zip(range(1,10), np.round(null_mean, 2)))}")

    # Single-DR diagnostic table
    print("\n" + "-"*72)
    print("Single-DR gaps (Torah vs Hebrew-letter Null)")
    print("-"*72)
    print(f"{'DR':<4} {'Torah %':<10} {'Null %':<10} {'Gap':<10}")
    for k in range(1, 10):
        print(f"{k:<4} {torah_dr_pct[k-1]:<10.2f} {null_mean[k-1]:<10.2f} "
              f"{torah_dr_pct[k-1] - null_mean[k-1]:+.2f}")

    # 84-subset scan
    props = closure_properties()
    subset_res = []
    for combo in combinations(range(1,10), 3):
        t = sum(torah_dr_pct[k-1] for k in combo)
        n_mean = sum(null_mean[k-1] for k in combo)
        # CI for this combo — sum across trials
        trial_combo = null_dr[:, [k-1 for k in combo]].sum(axis=1)
        n_lo = float(np.percentile(trial_combo, 2.5))
        n_hi = float(np.percentile(trial_combo, 97.5))
        gap = t - n_mean
        inside = n_lo <= t <= n_hi
        subset_res.append({
            "subset": list(combo),
            "torah_pct": round(t, 4),
            "null_mean_pct": round(n_mean, 4),
            "null_ci95_low": round(n_lo, 4),
            "null_ci95_high": round(n_hi, 4),
            "gap": round(gap, 4),
            "torah_inside_ci": bool(inside),
            "add_closed": props[combo]["add"],
            "mul_closed": props[combo]["mul"],
            "both_closed": props[combo]["both"],
        })

    subset_res.sort(key=lambda x: -x["gap"])

    print("\n" + "=" * 72)
    print("RANKING — 84 size-3 subsets by Torah-vs-null gap (top 15)")
    print("=" * 72)
    print(f"{'Rank':<5} {'Subset':<15} {'Torah%':<10} {'Null%':<10} "
          f"{'Gap':<9} {'Outside CI?':<13} {'Closed+×'}")
    print("-"*72)
    for i, r in enumerate(subset_res[:15]):
        closed = "✓BOTH" if r["both_closed"] else (
                 "+only" if r["add_closed"] else (
                 "×only" if r["mul_closed"] else ""))
        out = "✗OUTSIDE" if not r["torah_inside_ci"] else "inside"
        print(f"{i+1:<5} {str(tuple(r['subset'])):<15} {r['torah_pct']:<10.2f} "
              f"{r['null_mean_pct']:<10.2f} {r['gap']:<+9.2f} {out:<13} {closed}")

    # {3,6,9} rank
    target_rank = next(i for i, r in enumerate(subset_res)
                       if r["subset"] == [3,6,9]) + 1
    target = next(r for r in subset_res if r["subset"] == [3,6,9])
    top = subset_res[0]

    print("\n" + "=" * 72)
    print("TORAH VERDICT")
    print("=" * 72)
    print(f"Torah's TOP subset:  {tuple(top['subset'])}  gap +{top['gap']:.2f} pp  "
          f"closed+×={top['both_closed']}")
    print(f"{{3,6,9}} rank in Torah:  {target_rank} / 84  gap = +{target['gap']:.2f} pp")
    print(f"{{3,6,9}} outside CI:     {not target['torah_inside_ci']}")
    print(f"\nQuran reference: {{3,6,9}} rank 1 of 84, gap +7.24 pp")

    out = {
        "torah_observed": {
            "n_total": len(words),
            "n_composite": len(comp),
            "pct_369_composite": round(torah_369, 4),
            "dr_distribution_composite_pct": {
                str(k+1): round(v, 4) for k, v in enumerate(torah_dr_pct)},
        },
        "hebrew_letter_residue_mod3": {
            "r_equiv_0": round(100*r0/total, 4),
            "r_equiv_1": round(100*r1/total, 4),
            "r_equiv_2": round(100*r2/total, 4),
        },
        "null_composite_dr_mean_pct": {
            str(k+1): round(v, 4) for k, v in enumerate(null_mean)},
        "ranking": [{"rank": i+1, **r} for i, r in enumerate(subset_res)],
        "target_369": {"rank": target_rank, **target},
        "top_subset": {"rank": 1, **top},
    }
    with open(os.path.join(RESULTS, "results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {os.path.join(RESULTS, 'results.json')}")


if __name__ == "__main__":
    main(n_trials=300)
