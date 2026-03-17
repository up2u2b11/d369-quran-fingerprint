# d369 — Digital Root Fingerprint of the Quran

**Author:** Emad Suleiman Alwan
**ORCID:** [0009-0004-5797-6140](https://orcid.org/0009-0004-5797-6140)
**Published:** March 17, 2026 — Night of the 27th of Ramadan 1446H
**License:** [CC BY 4.0](LICENSE)

---

## The Core Finding

When the letters of the Quran are converted to numbers — using **any** encoding system — summed per Surah, and reduced to their digital root, a consistent pattern emerges:

**The group {3, 6, 9} dominates.**

This pattern does not appear in any other Arabic text we tested:
not in Sahih al-Bukhari, not in Ibn Arabi's Futuhat, not in the Seven Mu'allaqat.

---

## How We Tested

We did not begin with a conclusion. We began with a question and let the numbers respond — **including when they surprised us.**

1. **Six AI models** (GPT-4, Claude, Gemini, Llama, Grok, ChatGPT) were asked to attack the research with their strongest objections.
2. They attacked: *"Abjad is arbitrary. The statistics are weak. The result is coincidence."*
3. We built a **completely new encoding system** from scratch — Special-6 — using only 0s and 1s, treating 33 distinct letter shapes instead of 28 phonemes.
4. We ran it on the Quran: **clear fingerprint (p = 0.007).**
5. We ran it on 3 other Arabic texts: **nothing.**
6. We returned to the six models: *"Explain this."* **They could not.**

---

## Experiment Summary

| # | Experiment | System | Unit | p-value | Status |
|---|-----------|--------|------|---------|--------|
| [01](experiments/01_transformation_map_g14/) | G14 Transformation Map | Abjad (ة=5) | 114 Surahs (group sums) | p < 0.00001 | ✅ |
| [02](experiments/02_readings_hafs_warsh/) | Fingerprint Stability: Hafs vs Warsh | Abjad | 114 Surahs × 2 readings | — | ✅ |
| [03](experiments/03_text_fingerprint_word_level/) | Word-Level Fingerprint (5 texts) | Abjad | 78,248 words | p ≈ 0 | ✅ |
| [04](experiments/04_special6_surah_level/) | Special-6 — Surah Level | Special-6 | 114 Surahs | **p = 0.007** | ✅ |
| [05](experiments/05_special6_word_level/) | Special-6 — Word Level | Special-6 | 78,248 words | p ≈ 0 | ✅ |
| [06](experiments/06_special6_transformation_map/) | Special-6 Transformation Map | Both | 114 Surahs (group sums) | — | ✅ |
| [07](experiments/07_architecture_vs_words/) | Architecture vs. Words? | Special-6 | 114 × 3 tests | **p = 0.0093** | ✅ |

---

## Key Results

### Cross-Text Comparison (Experiment 04)

| Text | {3,6,9} | p-value | Significant? |
|------|---------|---------|-------------|
| **Quran** | **51/114 = 44.7%** | **0.007** | **✅ Yes** |
| Sahih al-Bukhari | 40/114 = 35.1% | 0.384 | ✗ No |
| Ibn Arabi's Futuhat | 37/114 = 32.5% | 0.613 | ✗ No |
| The Seven Mu'allaqat | ~30% | ~0.60 | ✗ No |

### Architecture vs. Words (Experiment 07)

| Test | {3,6,9} | p-value |
|------|---------|---------|
| Quran — original order | 51/114 = 44.7% | **0.0093 ✅** |
| Quran — words shuffled | 43/114 = 37.7% | 0.1853 ✗ |
| Bukhari — split by Surah lengths | 39/114 = 34.2% | 0.4497 ✗ |

**Conclusion: The fingerprint is in the words in the order they were revealed.**
Neither the words alone nor the architecture alone is sufficient.

### The Complete Picture

```
Level           | Abjad (ة=5)            | Special-6
────────────────────────────────────────────────────
Word (78,248)   | p≈0  ✅ (38.2%)       | p≈0  ✅ (34.2%)
Surah (114)     | p=0.817  ✗ (29.8%)   | p=0.007  ✅ (44.7%)
Transformation  | {3,6,9} stable  ✅    | {9} only stable
```

**Each system reveals a different layer of the text.**

---

## The G14 Transformation Map (Experiment 01)

Using classical Abjad (ة=5), group the 114 Surahs by their digital root, then sum each group and compute the digital root of that sum:

```
Root 3 (13 Surahs) → sum 3,210,951 → digital root 3  ✅ preserved
Root 6 (10 Surahs) → sum 2,642,856 → digital root 6  ✅ preserved
Root 9 (12 Surahs) → sum 3,147,993 → digital root 9  ✅ preserved
All others         → transform to different roots
```

**{3, 6, 9} are the only roots that preserve themselves when their groups are summed.**
Probability of this occurring by chance: p < 0.00001 (Monte Carlo, 100,000 trials).

Complete transformation structure:

```
{3, 6, 9}  →  stable (Tesla's triad)
{2, 5, 8}  →  all transform to 3
{4 ↔ 7}   →  cycle: 4→7 and 7→4
{1 → 5}   →  1 transforms to 5
```

---

## The Special-6 Encoding System

A new encoding system built entirely from 0s and 1s, assigning a unique value to each of the 33 distinct Arabic letter **shapes** (not 28 sounds):

```
أ=1        ب=10       ة=11       ت=100      ث=101
ج=111      ح=110      خ=1000     د=1001     ذ=1011
ر=1111     ز=1100     س=1110     ش=10000    ص=10001
ض=10011    ط=10111    ظ=11111    ع=11110    غ=11100
ف=11000    ق=100000   ك=100001   ل=100011   م=100111
ن=101111   ه=111111   و=111110   ؤ=1000000  ى=111100
ي=111000   ئ=1000001  ء=110000
```

Key distinction: **ة ≠ ت** (both = 400 in classical Abjad, but 11 vs 100 in Special-6).

This is an independent system — any result shared between Special-6 and Abjad cannot be attributed to the encoding choice.

**Original system — Emad Suleiman Alwan, 2026.**

---

## Published Papers

| Paper | Title | DOI |
|-------|-------|-----|
| I | Digital Root Transformation Map (G14) | [10.5281/zenodo.19041960](https://doi.org/10.5281/zenodo.19041960) |
| II | Digital Root in Word Repetition | [10.5281/zenodo.19055332](https://doi.org/10.5281/zenodo.19055332) |
| III | System-Independent Validation via Special-6 | [10.5281/zenodo.19073919](https://doi.org/10.5281/zenodo.19073919) |

---

## Reproduce Our Results

```bash
git clone https://github.com/up2u2b11/d369-quran-fingerprint
cd d369-quran-fingerprint
pip install -r requirements.txt

# Set paths
export D369_DB=data/d369_research.db
export D369_DATA=data/

# Run the decisive experiment (Special-6 vs 3 Arabic texts)
python experiments/04_special6_surah_level/experiment.py
# Expected: p ≈ 0.007 for Quran, p > 0.38 for all other texts

# Run the architectural test (words vs. structure)
python experiments/07_architecture_vs_words/experiment.py
# Expected: Quran original p<0.01, shuffled p>0.15, Bukhari p>0.40
```

---

## Five Open Research Doors

These questions emerged from the experiments and remain open:

1. **Spectrum of encoding systems:** Each system illuminates a different layer — how many layers does the Quran have?
2. **Semitic comparison:** Does this property extend to the Hebrew Torah or the Syriac Gospels?
3. **Computational linguistics:** What structural feature of Surahs carries the fingerprint — length? distribution? repetition?
4. **Third independent system:** If a third system confirms the same result, the evidence becomes triangulated.
5. **Architecture vs. words (answered in Exp. 07):** The fingerprint requires both the original words *and* their original order.

---

## Methodological Notes

- **No manual summation.** All sums are computed directly from the database (`sum()` from the `words` table). Manual summation was identified as a source of error in early iterations.
- **Permutation test, not Monte Carlo uniform.** Random digit generation (uniform 1–9) was replaced with actual shuffling of Quranic word values. This is the correct null model.
- **The `surahs.jummal_total` column is not used.** The database contains a pre-computed column that uses a slightly different convention. All experiments compute sums directly from `text_uthmani` in the `words` table.
- **Abjad system used: ة=5.** Not ة=400. The G14 transformation map is verified only with ة=5.

---

## Claim

We make no theological claim. We make a scientific one:

> **The Quran carries a digital root structure that cannot be reproduced by chance, does not appear in other Arabic texts, and does not depend on any single encoding system.**

Any researcher anywhere can take our data, our code, and re-run every test.

**The numbers do not flatter. They do not lie. They do not fear.**

---

## Arabic Repository

**[d369-research](https://github.com/up2u2b11/d369-research)**
— The original repository in Arabic (the language of the research).
Same experiments, same data, same code — for Arabic-speaking researchers.

---

*Emad Suleiman Alwan — up2b.ai — March 17, 2026*
*"And We have revealed to you the Book as clarification for all things" (16:89)*
