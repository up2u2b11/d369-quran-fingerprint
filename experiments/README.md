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

---

## Corresponding Papers

- Experiments 01–02 → [Paper I](https://doi.org/10.5281/zenodo.19041960)
- Experiment 03 → [Paper II](https://doi.org/10.5281/zenodo.19055332)
- Experiments 04–06 → [Paper III](https://doi.org/10.5281/zenodo.19073919)
- Experiment 07 → Paper IV (in preparation)
