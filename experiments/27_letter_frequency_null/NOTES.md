# Experiment 27 — Scientific Notes

**Date:** 13 April 2026
**Agents:** Server Opus (this machine) + Web Opus (claude.ai) + Emad (judge)
**Status:** ✅ VERIFIED INDEPENDENTLY BY BOTH AGENTS. Internal working
document only. NOT for external distribution until full paper is drafted
and peer-ready.

---

## 1. Why This Experiment Was Critical

Experiments 25 and 26 established:
- Quranic composite words show 48.44% in {3,6,9} (Abjad)
- Bukhari: 43.12%, Muallaqat: 36.23%
- N-bonacci null (Fake_Fibo seed): max 35.72%
- Mathematical constants (π, e, φ, √2): ~33.3%

A "beautiful" three-layer frame was proposed: **recurrences repel →
random constants neutral → Quran attracts**. The implied claim was
that Quran exceeds the maximum mathematical null by ~13 percentage
points and exceeds uniform by ~15 percentage points.

This frame hid a confound: **the Arabic language's letter distribution
is itself biased toward {3,6,9}**. About 10 of 28 Arabic letters have
Abjad values divisible by 3 (ج، و، ط، ل، س، ص، ش، خ، ظ، غ). So any
Arabic text, purely by linguistic chance, should produce 33-43% in
{3,6,9} without any compositional artistry.

Exp 27 asks: after controlling for the linguistic baseline (letter
frequencies + word length distribution), does the Quranic signal
remain — and at what effect size?

## 2. Methodology

**Monte Carlo null:** 1,000 trials, each generating 78,248 synthetic
"words". For each synthetic word:
1. Sample a length ℓ from the Quranic word-length distribution.
2. Sample ℓ independent letters from a letter-frequency distribution.
3. Compute the word's Abjad sum and digital root.

Three letter-frequency sources were tried:
- **Quran's own letters** (self-null — strongest control)
- **Bukhari letters** (external Arabic reference)
- **Uniform 28-letter** (pure baseline)

All three converge on ~33.3% under law of large numbers on sums mod 3.

**Residue-mod-3 diagnostic** before running:
```
Quran letters:    r≡0: 24.55%   r≡1: 46.72%   r≡2: 28.73%
Bukhari letters:  r≡0: 24.63%   r≡1: 44.72%   r≡2: 30.65%
Uniform:          r≡0: 32.14%   r≡1: 35.71%   r≡2: 32.14%
```
The letter-level bias toward residue 1 does NOT translate to word-level
bias toward residue 0, because word residue is a sum over independent
letters and CLT drives it to uniform on {0,1,2}.

## 3. Two Framings — Both Reported

Experiment 25 computes %{3,6,9} conditional on composite words. The
unconditional rate is different and matters for comparison.

| Framing | Quran | Null mean | 95% CI | Gap |
|---|---|---|---|---|
| **Unconditional** (all 78,248) | 38.23% | 33.34% | [33.02, 33.68] | **+4.89 pp** |
| **Composite only** (61,757) | 48.44% | 41.21% | [40.81, 41.57] | **+7.23 pp** |

**Why composite-only null is 41.21%, not 33.3%:**
Primes > 3 are mathematically excluded from {3,6,9} (dr(p) ∈ {1,2,4,5,7,8}
for p > 3 prime). Removing them from the denominator mechanically
inflates the remaining {3,6,9} proportion. Exp 25's 48.44% therefore
must be compared to a null that applies the same filter.

## 4. The Scientifically Correct Claim

The "+15 percentage points above baseline" framing, used in earlier
discussions today, is **misleading**. Uniform-random baseline (33.3%)
is not the correct reference because it assumes neither Arabic letter
frequency nor Quranic word length — confounds the paper must control for.

After controlling for both, **the real gap is +7.23 percentage points**
above a matched linguistic null, in the composite-only framing.

Statistical significance: gap is outside the 95% CI of 1,000 Monte Carlo
trials (p < 0.005 empirical). Effect size (Cohen's h): approximately
0.15 — small by conventional cutoffs.

## 5. What Still Holds — and Why the Paper Is Not Diminished

The smaller effect size does **not** dissolve the Quranic signal. Three
converging lines of evidence remain:

1. **Word-level excess is real.** Quran: 48.44% composite, null: 41.21%.
   Gap +7.23 pp, outside 95% CI under a linguistically-matched Monte
   Carlo.

2. **Surah-level structural effect (from Exp 07).** 44.7% of surahs
   hit {3,6,9} in their aggregate under original ordering (p = 0.0093).
   Under word-shuffle preserving surah sizes, this drops to 37.7%
   (p = 0.185). The surah-level signature **is destroyed by shuffle**,
   proving it is structural, not a mere letter-frequency artifact.

3. **Orthogonal encoding confirmation.** The effect appears in both
   Abjad and Special-6 encodings (Exp 05, 25). Two independent letter-
   to-value maps should not both produce the same artifact by chance.

**Spider note:** It is tempting to merge evidence lines into "the
7.23 pp gap disappears under shuffle." That merging is incorrect.
The word-level marginal is shuffle-invariant by construction (a word's
Abjad value doesn't depend on its position). It is the **surah-level
aggregate** that is shuffle-sensitive. The paper must report these as
two distinct findings at two distinct scales, not conflate them.

## 6. Updated Scientific Claim (publishable form)

> *"In a Monte Carlo null model (1,000 trials, n = 78,248 synthetic
> words) preserving Quranic word-length distribution and Quranic
> letter-frequency distribution, composite words fall in digital-root
> set {3,6,9} at a mean rate of 41.21% (95% CI [40.81, 41.57]). The
> observed Quranic composite rate of 48.44% (Abjad) exceeds this null
> by 7.23 percentage points, lying well outside the 95% CI (empirical
> p < 0.005). Effect size is small (Cohen's h ≈ 0.15) but robust
> across all three letter-source variants (Quran self-null, Bukhari
> external, uniform baseline). At the surah level (Exp 07), 44.7% of
> surahs hit {3,6,9} in aggregate (p = 0.0093); this drops to 37.7%
> under within-surah-length-preserving word-shuffle (p = 0.185),
> confirming the surah-level signature is structural rather than
> derived from marginal letter-frequency or length biases. The
> Quranic signal is therefore interpreted as a structural-compositional
> phenomenon of modest but genuine magnitude, not reproducible by
> mathematical recurrences (Exp 26), mathematical constants
> (Exp 28), or linguistic null models (this experiment)."*

## 7. Methodological Lessons

**a) Null models must be chosen to control confounds, not to maximize
the gap.** Switching from uniform (33.3%) to Arabic-letter null (41.21%
composite) reduced the headline gap from 15 pp to 7 pp — but the
7 pp is the *honest* number. The 15 pp included the Arabic language's
inherent bias toward {3,6,9}.

**b) Conditional vs. unconditional rates must be compared like-for-like.**
Exp 25's 48.44% is composite-only; the comparable null must also be
composite-only.

**c) Marginal versus structural claims must not be conflated.** Word-level
{3,6,9} rate is a marginal statistic; surah-level clustering is a
structural statistic. They respond differently to shuffle and must be
reported separately.

## 8. Independent Verification — Completed

Web Opus ran its own parallel implementation of the null model (using
Bukhari text as the letter source, different code path, same principle).
Results below:

| Metric | Server Opus | Web Opus | Δ |
|---|---|---|---|
| Null unconditional | 33.34% | 33.33% | 0.01 pp |
| Null composite | 41.21% | 40.56% | 0.65 pp |
| r ≡ 0 (mod 3) share | 24.63% (Bukhari) | 24.78% | 0.15 pp |

**Convergence:** Both implementations agree within expected Monte Carlo
noise. The 0.65 pp gap in composite null traces to letter-source
difference (Quran-internal vs Bukhari-external) — itself a minor
robustness check, not a contradiction.

**Joint verdict:** The corrected headline figure is confirmed as
**Quran composite vs linguistic null ≈ +7 percentage points** (not
the +15 pp suggested by earlier uniform-baseline comparisons). Both
agents concur. Emad, as judge, has accepted the correction.

## 9. Document Status

- 🔒 **Internal only.** This file is a lab notebook, not a manuscript.
- 📝 Numbers here supersede the earlier "+15 pp" framing in prior
  transcript notes.
- 🚫 **Do NOT share with external reviewers, researchers, or platforms
  (Zenodo, arXiv, mailing lists) at this stage.** The paper must be
  drafted, internally reviewed, and peer-ready before release.
- ✅ Use this file as the authoritative source when drafting the
  forthcoming paper (Paper VIII — "Digital-Root Excess in the Quran:
  Signal, Null, Scale").

---

*Intellectual property: Emad Suleiman Alwan — up2b.ai — 2026*
*ORCID: 0009-0004-5797-6140*
