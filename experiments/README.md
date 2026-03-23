# Experiment Index

**Intellectual property:** Emad Suleiman Alwan — up2b.ai

---

## Overview

| # | Experiment | System | Unit | p-value | Status |
|---|-----------|--------|------|---------|--------|
| [01](01_transformation_map_g14/) | G14 Transformation Map | Abjad (ة=5) | 114 Surahs (group sums) | p < 0.00001 | ✅ |
| [02](02_readings_hafs_warsh/) | Fingerprint Stability: Hafs vs Warsh | Abjad | 114 Surahs × 2 readings | — | ✅ |
| [03](03_text_fingerprint_word_level/) | Word-Level Fingerprint (5 texts) | Abjad | 78,248 words | p ≈ 0 | ✅ |
| [04](04_special6_surah_level/) | Special-6 — Surah Level | Special-6 | 114 Surahs | **p = 0.007** | ✅ |
| [05](05_special6_word_level/) | Special-6 — Word Level | Special-6 | 78,248 words | p ≈ 0 | ✅ |
| [06](06_special6_transformation_map/) | Special-6 Transformation Map | Both | 114 Surahs (group sums) | — | ✅ |
| [07](07_architecture_vs_words/) | Architecture vs. Words? | Special-6 | 114 × 3 tests | **p = 0.0093** | ✅ |
| [08](08_division_architecture/) | Gate Five — Architecture of Division | Special-6 | 78,248 × 4 splits | **p = 0.007 / 0.010** | ✅ |
| [09](09_bukhari_control/) | Gate Six — Bukhari Control Group | Special-6 | 1,000 hadith × 4 splits | **p > 0.13 all** | ✅ |
| [10](10_torah_hebrew_control/) | Gate Seven — Torah (Hebrew) Control | Gematria | 69,196 words × 4 splits | **p > 0.33 all** | ✅ |
| [11](11_contribution_analysis/) | Gate Eight — Contribution Analysis (Leave-One-Out) | Special-6 | 114 × 3,000 trials | **all neutral** | ✅ |
| [12](12_torah_g14_map/) | Gate Nine — Torah G14 Transformation Map | Gematria | 54 Parashot + 5,846 verses | **p = 0.068 (not significant)** | ✅ |
| [13](13_ayah_count_fingerprint/) | Gate Ten — Verse-Count Fingerprint | No encoding | 114 Surahs + 54 Parashot | **p = 0.652 (not significant)** | ✅ |
| [14](14_random_encoding_test/) | Random Encoding Stress Test | 33 random | 114 Surahs × 33 encodings | **0/33 beat Special-6** | ✅ |
| [15](15_freq_order_encoding/) | System 3: Frequency Order Encoding | Freq-Order | 114 Surahs + 78K words | **5 self-preserving (p=0.0015)** | ✅ |
| [16](16_rasm_readings/) | Ten Canonical Readings + Uthmani vs. Imla'i Script | Abjad + K6 | 114 Surahs × 14 readings × 2 scripts | **p=0.011 (Imla'i) / p≈0 (word-level)** | ✅ |

---

## How to Run

```bash
# Requirements
pip install scipy

# Set database path
export D369_DB=/path/to/d369_research.db
export D369_DATA=/path/to/data/

# Run an experiment
python experiments/01_transformation_map_g14/experiment.py
python experiments/04_special6_surah_level/experiment.py
# ... etc.
```

---

## Shared Module

`shared/utils.py` contains:
- `JUMMAL_5` — Classical Abjad dictionary (ة=5)
- `JUMMAL_400` — Abjad with ة=400
- `KHASS_6` — Special-6 encoding (33 shapes)
- `digit_root(n)` — Digital root function
- `word_value(text, system)` — Word value under any system

---

## The Complete Picture

```
Level           | Abjad (ة=5)            | Special-6
────────────────────────────────────────────────────
Word (78,248)   | p≈0  ✅ (38.2%)       | p≈0  ✅ (34.2%)
Surah (114)     | p=0.817  ✗ (29.8%)   | p=0.007  ✅ (44.7%)
Transformation  | {3,6,9} stable  ✅    | {9} only stable
```

**Each system sees a different layer — Abjad sees the word, Special-6 sees the Surah.**

### Control Group Results (Gates 6–7)

```
Text        Language  System    Division          p-value   Result
──────────────────────────────────────────────────────────────────
Quran       Arabic    Special-6 Surahs (divine)   0.007     ✅ peak
Quran       Arabic    Special-6 Verses (natural)  0.010     ✅
Bukhari     Arabic    Special-6 Natural hadith    0.139     ✗
Torah       Hebrew    Gematria  Natural Parashot   0.549     ✗
```

### Gate Eight Result (Experiment 11)

```
Leave-one-out × 114 Surahs (3,000 trials each):

🔴 Load-bearing:  0 Surahs
◻  Neutral:      114 Surahs
🟢 Booster:       0 Surahs
```

**The fingerprint is indivisible — it requires all 114 Surahs as a complete architecture.**

### Experiment 16 Result (Readings + Script)

```
Ten canonical readings: identical — fingerprint is reading-invariant ✅
Imla'i script:  K6=45% p=0.011 ✅ (Surah level)
Uthmani script: word-level p≈0 ✅ (stronger: z=34 vs z=27)
Invariant Core: 12 Surahs unaffected by either script
Letter dots:    part of the code — merging them destroys the fingerprint
```

---

## Corresponding Papers

- Experiments 01–02 → [Paper I](https://doi.org/10.5281/zenodo.19041960)
- Experiment 03 → [Paper II](https://doi.org/10.5281/zenodo.19055332)
- Experiments 04–06 → [Paper III](https://doi.org/10.5281/zenodo.19073919)
- Experiments 07–10 → [Paper IV](https://doi.org/10.5281/zenodo.19078371)
- Experiment 11 → [Paper V](https://doi.org/10.5281/zenodo.19079630)
- Experiment 12 → Paper VI (Torah lacks G14 architecture)
- Experiments 01–16 → [Comprehensive Paper](https://doi.org/10.5281/zenodo.19176486)
