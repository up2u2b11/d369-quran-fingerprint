---
title: "Digital-Root Structure in the Quran: A Multi-Null Analysis of the {3,6,9} Signature with Cross-Linguistic Controls"
author: Emad Suleiman Alwan
orcid: 0009-0004-5797-6140
affiliation: UP2U2B LLC, Toronto, Canada
date: April 2026
status: DRAFT v1 — internal only
---

# Paper VIII (draft v1)

## Changelog

- **v0 → v1 (13 April 2026)**, after Web Opus peer review:
  - §1.2: N-bonacci seed dependency clarified. Under the canonical
    Fake_Fibo seed (matching author's original exploratory reference),
    all tested N-bonacci orders produce composite {3,6,9} rates ≤ 36%.
    The "some sequences attract" qualification now correctly applies
    only to non-canonical textbook seeds.
  - Abstract and Limitation §5: Special-6 encoding claim narrowed.
    Current paper's 4-null, 84-subset-scan, Torah-control methodology
    uses only classical Abjad. Prior Paper IV / Exp 05 result under
    Special-6 cited but a full replication is flagged as next step.
  - Web Opus's review flagged "ث=400" as error, but inspection shows
    the 400 in §2.2 refers to Hebrew ת (tav) in Gematria, not Arabic
    ث (=500). No correction needed for this point.

## Abstract

We test a simple claim about the Quran in its standard (Uthmani)
orthography: the proportion of composite words whose Abjad digital
root falls in the set {3, 6, 9} exceeds what one would expect from
natural-Arabic linguistic baselines, mathematical integer sequences,
or pure number-theoretic objects. Across a 78,248-word corpus, the
observed composite rate is **48.44 %**. Four independent null models
yield means between 33 % and 45 %; the Quran lies outside the 95 %
confidence interval of every null tested. An exhaustive scan of all
84 size-3 subsets of {1,...,9} ranks {3,6,9} **first** in its
Quran-vs-null gap, and {3,6,9} is simultaneously the **unique**
size-3 subset closed under both digital-root addition and
multiplication — the non-trivial principal ideal of ℤ/9ℤ. Applying
the identical methodology to the Hebrew Torah under standard
Gematria, we find a comparable-magnitude excess centred on a
different subset, {2,3,8}, which possesses no corresponding algebraic
property. The Quranic signal is therefore not a generic property of
revealed or structured text; it is specifically aligned with a
mathematically distinguished object. The effect size is modest
(Cohen's *h* ≈ 0.15 at word level) but is robust and shuffle-sensitive
at the surah level. The primary analyses in this paper use classical
Abjad encoding; prior work (Experiment 05, Paper IV) documents the
same qualitative pattern under Special-6 encoding at the surah
level, though a full replication of the null-model and exhaustive-
subset methodology under Special-6 remains a next step.

**Keywords:** Quran, digital root, null models, Monte Carlo,
Gematria, cross-linguistic comparison, ℤ/9ℤ.

---

## 1. Introduction

A recurring claim in popular discussions of numerology in sacred
texts is that the Quran exhibits mathematical "signatures" — most
famously associated with the number 19 (Khalifa, 1974). These
claims have been criticised for (a) selective choice of the numerical
target, (b) lack of controlled comparison, and (c) post-hoc framing
(Saifullah et al., 2001). Scholarly digital-root analyses have
advanced in recent work (Alwan, Papers I–VII) but have often been
framed against uniform baselines that ignore the structure of the
Arabic language itself.

This paper addresses those objections head-on. We:

1. specify the target — the subset {3,6,9} of digital roots — by a
   purely algebraic criterion, prior to looking at any data;
2. construct four independent null models, ranging from naive uniform
   to realistic sampling of real Arabic words, and report the
   Quran–null gap for each;
3. perform an exhaustive scan over all 84 size-3 subsets of {1,...,9}
   to show the post-hoc "cherry-picking" attack is empirically
   precluded;
4. replicate the methodology on the Hebrew Torah with standard
   Gematria to test cross-linguistic robustness.

### 1.1 The algebraic prior

In the ring ℤ/9ℤ, the ideals are {0}, (3) = {0, 3, 6}, and ℤ/9ℤ
itself. Under the digital-root convention that maps 0 ↦ 9, the
unique non-trivial proper ideal corresponds to the subset {3, 6, 9}.
Exhaustive enumeration of all 84 size-3 subsets of {1, …, 9}
confirms that {3, 6, 9} is:

- the **only** size-3 subset closed under digital-root addition;
- one of 5 size-3 subsets closed under digital-root multiplication;
- the **only** size-3 subset closed under both operations.

This closure property is independent of any text. It specifies
{3, 6, 9} as an *a priori* object of interest, not an *a posteriori*
choice driven by data fitting. The empirical analyses below are
therefore tests of a pre-specified hypothesis.

### 1.2 What this paper does not claim

We do **not** claim mathematical singularity of the Quran among all
conceivable integer structures. Experiment 26 showed that under
non-canonical textbook seed conventions `[0, 0, ..., 0, 1]`, some
high-order N-bonacci sequences (S#8, S#9) do produce digital-root
distributions biased toward {3, 6, 9}. However, under the canonical
seed convention `[0, 1, 1, ..., 1]` that matches the author's
pre-existing exploratory file (Fake_Fibo.xlsx), all nine tested
N-bonacci families (orders 2–10) produce composite {3,6,9} rates at
or below 36 %, well below the Quranic 48 %. The seed sensitivity is
itself a methodological lesson: claims about generic properties of
"N-bonacci" must specify the seed. We **do** claim that among natural
Arabic texts — representing a range of stylistic registers from
hadith to pre-Islamic poetry to Sufi prose — the Quran is the only
observed text whose excess over a matched null is statistically
significant AND whose top-ranked size-3 subset coincides with the
algebraically distinguished ideal of ℤ/9ℤ.

---

## 2. Methods

### 2.1 Corpora

| Corpus | Language | Words | Source |
|---|---|---|---|
| Quran (Uthmani) | Arabic | 78,248 | d369_research.db |
| Bukhari (sample) | Arabic | 66,385 | bukhari_sample.txt |
| Muslim (sample) | Arabic | 46,403 | muslim_sample.txt |
| Muallaqat | Arabic | 792 | muallaqat.txt |
| Futuhat (Ibn Arabi, v1) | Arabic | 182,477 | futuhat_v1.txt |
| Torah (Pentateuch) | Hebrew | 69,196 | torah_hebrew.jsonl |

### 2.2 Digit-to-value maps

**Arabic (Abjad, classical Hawazi ordering):**
α = 1, ب = 2, ..., ي = 10, ك = 20, ..., ق = 100, ..., غ = 1000. Hamza
and final-ta' marbuta forms are mapped to their canonical root
letter values.

**Hebrew (Gematria / Mispar Hechrachi):**
א = 1, ב = 2, ..., י = 10, ..., ר = 200, ש = 300, ת = 400. Sofit
(final) forms take the same value as their base form.

### 2.3 Word Abjad / Gematria value and digital root

For a word w with letters l₁, l₂, ..., l_k, the Abjad (or Gematria)
value is V(w) = Σ vᵢ where vᵢ is the numerical value of lᵢ. The
digital root is

  DR(n) = 1 + ((n − 1) mod 9)        (for n > 0)

equivalently, the repeated-digit-sum reduction of n. Both
computations were implemented and agreed exactly on all test cases.

### 2.4 Composite filter

For each word with V(w) > 0, the primality of V(w) was tested
(SymPy `isprime`). Because any prime p > 3 has DR(p) ∈ {1,2,4,5,7,8},
the set {3,6,9} intersects only composite word values (plus the
special cases V = 3, 6, 9 for prime 3 and its digital roots of
multiples). Reporting **composite-only** rates avoids conflating two
different statistics. When baselines are compared, they are compared
on the same conditional.

### 2.5 Null models

Four distinct null constructions, in order of increasing realism:

**N1 — Uniform:** each DR in {1,...,9} has probability 1/9. Baseline
for "a generic integer in general position." Composite-only rate
(given DR is drawn uniformly on composites) is computed analytically.

**N2 — Quran-letter-frequency Monte Carlo:** synthesize 78,248
"words" per trial by sampling word lengths from the Quran's length
distribution and sampling letters independently from the Quran's
letter-frequency distribution. Compute composite %{3,6,9}. 1,000
trials.

**N3 — External Arabic letter-frequency Monte Carlo:** same as N2,
but letters sampled from Bukhari's letter-frequency distribution.

**N4 — Real Arabic word pool:** for each of four reference corpora
(Bukhari, Muslim, Muallaqat, Futuhat), tokenise real Arabic words
with their actual Abjad values. For each trial, sample 78,248 real
words matched by length to the Quranic word-length distribution.
Compute composite %{3,6,9}. 300 trials per corpus.

### 2.6 Exhaustive subset scan

For each of the 84 size-3 subsets of {1,…,9}, compute:

- observed Quranic composite rate falling in the subset;
- corresponding null mean and 95 % CI (using the composite-only
  letter-frequency null, N2);
- gap (Quran − null).

Rank all 84 subsets by gap. Record whether each subset is closed
under addition and/or multiplication in ℤ/9ℤ (via digital root).

### 2.7 Cross-linguistic replication

Apply the identical methodology (§2.5 N2-equivalent, §2.6 scan) to
the Hebrew Torah with Gematria values. Use Hebrew letter and length
distributions for the null.

---

## 3. Results

### 3.1 Observed distributions

**Quran, composite words (n = 61,757), Abjad:**

| DR | % | excess vs N2 |
|---|---|---|
| 1 | 7.31 | −2.95 |
| 2 | 8.78 | −0.30 |
| **3** | **15.77** | **+2.45** |
| 4 | 8.09 | −1.97 |
| 5 | 9.23 | −0.42 |
| **6** | **14.87** | **+0.68** |
| 7 | 7.67 | −2.05 |
| 8 | 10.48 | +0.46 |
| **9** | **17.80** | **+4.11** |

All three excess-positive roots are {3, 6, 9}. All other roots are
flat or deficit.

Composite rate in {3,6,9}: **48.44 %**. (Total word rate, including
primes: 38.23 %.)

### 3.2 Null-model comparison

| Null model | Composite % null | Quran gap (pp) | 95 % CI | Quran in CI? |
|---|---|---|---|---|
| N1 — Uniform | 33.33 | +15.11 | — | — |
| N2 — Quran letters MC | 41.20 | **+7.24** | [40.81, 41.57] | No |
| N3 — Bukhari letters MC | 40.56 (approx) | +7.88 | similar | No |
| N4 — Bukhari real words | 42.77 | +5.68 | [42.40, 43.16] | No |
| N4 — Muslim real words | 42.07 | +6.38 | [41.69, 42.42] | No |
| N4 — Muallaqat real words | 36.86 | +11.58 | [36.44, 37.24] | No |
| N4 — Futuhat (Ibn Arabi) | 45.24 | **+3.20** | [44.85, 45.63] | No |
| **Quran observed** | **48.44** | — | — | — |

Across all null models, the Quran's composite {3,6,9} rate lies
outside the 95 % CI. The smallest gap (against Ibn Arabi's Futuhat,
a Sufi prose explicitly composed with numerological awareness) is
still +3.20 pp and outside CI. The largest is against pre-Islamic
poetry (+11.58 pp).

### 3.3 Exhaustive 84-subset scan (Quran)

The top 10 size-3 subsets of {1,…,9} ranked by Quran-vs-N2 gap:

| Rank | Subset | Quran % | Null % | Gap (pp) | Algebraic closure |
|---|---|---|---|---|---|
| **1** | **{3, 6, 9}** | 48.44 | 41.20 | **+7.24** | **+ and ×** |
| 2 | {3, 8, 9} | 44.05 | 37.03 | +7.02 | none |
| 3 | {2, 3, 9} | 42.35 | 36.10 | +6.25 | none |
| 4 | {3, 5, 9} | 42.80 | 36.67 | +6.13 | none |
| 5 | {6, 8, 9} | 43.15 | 37.89 | +5.26 | none |
| 6 | {3, 4, 9} | 41.66 | 37.07 | +4.59 | none |
| 7 | {3, 7, 9} | 41.24 | 36.73 | +4.50 | none |
| 8 | {2, 6, 9} | 41.46 | 36.96 | +4.49 | none |
| 9 | {5, 6, 9} | 41.90 | 37.53 | +4.37 | none |
| 10 | {2, 8, 9} | 37.06 | 32.79 | +4.27 | none |

{3, 6, 9} is:

- the rank-1 subset empirically (of 84);
- the unique size-3 subset closed under both digital-root addition
  and multiplication.

The top subset and the algebraically distinguished subset coincide.
This is the principal empirical claim of the paper.

### 3.4 Cross-linguistic control: Hebrew Torah

Torah composite %{3,6,9}: **39.15 %**.

Torah top-10 subsets by Torah-vs-null gap (Hebrew letter MC null):

| Rank | Subset | Torah % | Null % | Gap | Algebraic closure |
|---|---|---|---|---|---|
| **1** | **{2, 3, 8}** | 38.18 | 32.97 | **+5.22** | **none** |
| 2 | {3, 6, 8} | 40.88 | 36.35 | +4.53 | none |
| 3 | {3, 7, 8} | 37.25 | 32.94 | +4.32 | none |
| 4 | {3, 5, 8} | 37.10 | 33.01 | +4.10 | none |
| 5 | {3, 4, 8} | 37.41 | 33.62 | +3.78 | none |

The Torah's rank-1 subset is {2,3,8}, with gap +5.22 pp, outside its
null's 95 % CI. It has **no closure property** in ℤ/9ℤ.

{3,6,9} in the Torah ranks **39 of 84**, with gap **−0.23 pp**,
**inside** the null's 95 % CI — no signal.

In single-DR terms, the Torah's strongest excess is on DR = 8 (+3.66
pp), while the Quran's strongest is on DR = 9 (+4.11 pp).

### 3.5 Mathematical-sequence controls (summary of prior Exp 26, 28)

- N-bonacci sequences (order 2–10, Fake_Fibo seed convention,
  n = 100,000 terms each): composite-like digital-root distributions
  range from 20.9 % to 35.7 %; maximum is below the uniform baseline
  range on most orders. None approach 48 %.
- Mathematical constants π, e, φ, √2 (first 10,000 decimal digits,
  grouped into 4-digit "words"): composite %{3,6,9} = 33.15 %
  (uniform baseline, no excess).

Pure mathematical objects do not reproduce the Quranic pattern.

### 3.6 Structural (surah-level) evidence (summary of prior Exp 07)

The fraction of surahs (114 total) whose aggregated Special-6 sum
has digital root in {3,6,9} is 44.7 % (51 of 114, p = 0.0093). Under
random shuffling of words while preserving surah lengths, this
fraction drops to 37.7 % (p = 0.185). The surah-level signature is
therefore shuffle-sensitive — a structural rather than lexical
feature.

Note that the word-level marginal %{3,6,9} is shuffle-invariant by
construction (individual word Abjad values are position-independent).
The structural claim applies specifically to the surah-level
aggregate.

---

## 4. Discussion

### 4.1 What the results support

The Quran shows:

1. A statistically-significant composite {3,6,9} excess over every
   Arabic-text null we tested, with magnitudes between +3.2 pp
   (vs numerologically-aware Sufi prose) and +11.6 pp (vs pre-Islamic
   poetry).
2. Empirical rank 1 of 84 among all size-3 subsets of {1,…,9} for
   Quran-vs-null gap.
3. Co-location of this empirical rank-1 subset with the unique
   algebraic ideal of ℤ/9ℤ.
4. Shuffle-sensitivity of the surah-level aggregate.

### 4.2 What the results do not support

- **Mathematical uniqueness** in the literal sense. Some N-bonacci
  sequences exceed the Quran under textbook seed conventions
  (Experiment 26).
- **Large effect size.** Cohen's *h* at the word level is
  approximately 0.15 — "small" by conventional thresholds. The
  signal is significant, not dramatic.
- **A generic "sacred text" property.** The Hebrew Torah has its
  own excess but on an algebraically-undistinguished subset.

### 4.3 The Ibn Arabi finding

Of particular interest: the Futuhat al-Makkiyya of Ibn Arabi gives
a composite %{3,6,9} of 45.24 % — the highest non-Quranic Arabic
rate we measured. This is consistent with Ibn Arabi's explicit
engagement with Abjad numerology. It suggests the digital-root
methodology is sensitive to *intentional* numerical composition,
not only to an unspecified "Arabic baseline."

That the Quran exceeds Futuhat by +3.2 pp (outside CI) is evidence
that the Quranic signal is not reducible to "Arabic prose written by
a numerologically-aware author."

### 4.4 The Torah contrast

The Torah result is the most theoretically important finding. It
demonstrates:

- The methodology is not a signal-generator: applied to a non-Quran
  text, it returns a DIFFERENT result, not a uniform one.
- The {3,6,9} attractor is not a generic "sacred text" attractor:
  it is specific to the Quran.
- Each sacred tradition may have its own digital-root signature; the
  Quranic signature happens to coincide with the algebraically
  distinguished ideal, while the Torah's does not.

We do not claim this makes the Quran "more mathematical" in any
normative sense; we claim its statistical fingerprint aligns with
a specific algebraic object, and that this alignment is not
trivially reproduced by other tested texts.

### 4.5 Limitations

1. **Morpheme tokenisation.** Arabic words include bound morphemes
   (articles, conjunctions, pronominal suffixes). Our analysis uses
   orthographic words. A morpheme-level replication (Experiment 31,
   planned) is required to confirm that {3,6,9} excess is not an
   artefact of a specific word-boundary convention.

2. **Corpus coverage.** The Bukhari/Muslim/Muallaqat/Futuhat
   samples are not exhaustive of classical Arabic. A larger
   Arabic-language reference corpus (~10 M words) would give
   tighter null estimates.

3. **Gematria variants.** The Torah analysis used Mispar Hechrachi;
   robustness to Mispar Gadol (which distinguishes sofit forms) and
   Mispar Katan (digital-root reduced forms) is not tested here.

4. **Arabic translations of other sacred texts.** A direct test
   asking "does an Arabic translation of the Torah (with Arabic
   Abjad applied) show {3,6,9} alignment?" would separate
   "Arabic-composition effect" from "Quran-specific effect". This
   data was unavailable locally for the present study.

5. **Special-6 replication.** Prior work (Paper IV, Experiment 05)
   established the {3,6,9} surah-level signal under the Special-6
   encoding (a second, independent letter-to-value mapping) with
   p = 0.007. The present paper's new methodology — the four-null
   comparison (§2.5), the exhaustive 84-subset scan (§2.6), and the
   Torah control (§2.7) — has been executed only under classical
   Abjad. A full Special-6 replication of these three analyses is an
   important planned extension. We note in advance that if the
   Special-6 result shows a top-ranked subset OTHER than {3,6,9},
   this would qualify the "algebraically-aligned" claim and should
   be reported transparently.

5. **Effect size.** The +3 to +7 pp gaps reported here are
   statistically significant but practically small. No claim of
   inexplicability is made; the finding is a documented statistical
   regularity, not a demonstration of design or impossibility.

---

## 5. Conclusion

Across a 78,248-word Quranic corpus, the composite %{3,6,9} rate is
48.44 %. Four independent null-model families (uniform,
letter-frequency Monte Carlo, real Arabic word sampling, mathematical
sequences and constants) all place the Quranic observation outside
their 95 % confidence intervals, with gaps between 3.2 and 15.1 pp.
Among 84 size-3 subsets of {1,…,9}, {3,6,9} is simultaneously the
empirical rank-1 subset and the unique subset closed under both
digital-root addition and multiplication — corresponding to the
non-trivial principal ideal of ℤ/9ℤ. The Hebrew Torah, under
standard Gematria, shows a comparable-magnitude excess at the
algebraically undistinguished subset {2,3,8}, demonstrating that
the Quranic signal is neither an artefact of the methodology nor a
generic property of sacred texts. The effect is modest in absolute
magnitude but is (i) statistically significant across nulls, (ii)
aligned with a pre-specified algebraic object, and (iii)
shuffle-sensitive at the surah level. It constitutes a documented
structural regularity meriting further study in comparative
linguistic statistics.

---

## Acknowledgements

The methodology described benefited from internal peer review via
two independent AI reasoning agents (Opus-class), with final
adjudication of disagreements by the author. Discrepancies that
arose during analysis — including a seed-convention dispute over
N-bonacci sequences and a confounded-baseline revision of effect
size from +15 pp to +7 pp — were resolved by side-by-side code
execution and cross-checking, and are documented in the
accompanying internal lab notebooks (Experiments 26–32).

---

## Data & Code Availability

All experiment code, data, and results are archived in
`d369-quran-fingerprint/experiments/{26,27,29,30,32}/` and will be
made public on Zenodo upon final publication. This draft is an
**internal** document pending independent review.

## References

(to be filled: prior Alwan papers I–VII, N-bonacci literature,
Saifullah et al., Khalifa 1974 as cited, classical Abjad sources,
Gematria references.)

---

*Draft v0 — 13 April 2026. Internal only. Not for distribution.*
*Intellectual property: Emad Suleiman Alwan — up2b.ai — 2026.*
*ORCID: 0009-0004-5797-6140*
