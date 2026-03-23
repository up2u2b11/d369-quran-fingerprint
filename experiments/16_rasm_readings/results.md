# Experiment 16 — Ten Canonical Readings + Uthmani vs. Imla'i Script

**Date:** March 22, 2026  
**Researcher:** Emad Suleiman Alwan | ORCID: 0009-0004-5797-6140  
**Source:** 14 Quranic recitations from tanzil.net v1.1 | CC-BY 3.0

---

## Objective

Test the stability of the {3,6,9} digital root fingerprint across:
1. Ten mutawātir canonical readings (Hafs, Warsh, Qalun, Shu'ba, al-Duri, al-Susi, al-Bazzi, Qunbul, Hisham, Khalaf, Ruwais)
2. Two orthographic conventions: Uthmani rasm (tanzil.net) vs. modern Imla'i spelling (quran_simple_clean)

---

## Part I: Ten Canonical Readings — Identical Results

| Reading | Abjad {3,6,9} | K6 {3,6,9} | Words |
|---------|--------------|------------|-------|
| Hafs (Uthmani) | 33/114=29% | 30/114=26% | 77,881 |
| Warsh | 33/114=29% | 30/114=26% | 77,881 |
| Qalun | 33/114=29% | 30/114=26% | 77,881 |
| Shu'ba | 33/114=29% | 30/114=26% | 77,881 |
| al-Duri | 33/114=29% | 30/114=26% | 77,881 |
| al-Susi | 33/114=29% | 30/114=26% | 77,881 |
| al-Bazzi | 33/114=29% | 30/114=26% | 77,881 |
| Qunbul | 33/114=29% | 30/114=26% | 77,881 |
| Hisham | 33/114=29% | 30/114=26% | 77,881 |
| Khalaf | 33/114=29% | 30/114=26% | 77,881 |
| Ruwais | 33/114=29% | 30/114=26% | 77,881 |

**Conclusion:** The differences among the ten canonical readings are too small to affect the digital root of any Surah. The fingerprint is **reading-invariant**. This question is closed.

---

## Part II: Uthmani vs. Imla'i Script

### Surah-Level Results

| Convention | K6 {3,6,9} | p-value | Abjad {3,6,9} |
|-----------|-----------|---------|---------------|
| Imla'i (quran_simple_clean) | 51/114=**45%** | **0.011** | 46/114=40% |
| Uthmani (tanzil.net) | 30/114=**26%** | ~0.96 | 33/114=29% |

### Word-Level Results (Invariant Across Scripts)

| Convention | K6 {3,6,9} | z-score | Abjad {3,6,9} | z-score |
|-----------|-----------|---------|---------------|---------|
| Imla'i | 26,753/78,248=34.2% | z=5.08 | 29,689/78,248=37.9% | z=27.35 |
| Uthmani | 27,493/77,881=35.3% | z=11.65 | 30,445/77,881=39.1% | z=34.09 |

**p≈0 in both scripts and both encodings at word level. The word-level fingerprint is orthographically invariant.**

---

## Part III: Scale of Orthographic Effect

- **102 of 114 Surahs** (90%) change K6 digital root between scripts
- **12 Surahs** unchanged — the Invariant Core
- **35 Surahs** left {3,6,9} (Imla'i → Uthmani)
- **14 Surahs** entered {3,6,9}

### Root Causes — 16,534 Orthographic Word Differences

| Pattern | Count | Example |
|---------|-------|---------|
| ي/ى alternation (في → فى) | **1,125** | في/فى, الذي/لذى |
| Hamza form (آ → ءا) | 252 | آمنوا/ءامنوا |
| Vowel letter (الصلاة → الصلوة) | 68 | الصلاة/الصلوة |
| Internal alif deletion | 436+ | الكتاب/لكتب |

**Basmala hypothesis refuted:** The Basmala is identical in both scripts (K6=1,027,164).

---

## Part IV: The Invariant Core — 12 Unchanged Surahs

| Surah | K6 DR | ∈ {3,6,9} |
|-------|-------|-----------|
| Āl 'Imrān (3) | 1 | |
| Al-Anfāl (8) | **6** | ✅ |
| Al-Ra'd (13) | **6** | ✅ |
| Ghāfir (40) | 5 | |
| Al-Munāfiqūn (63) | 2 | |
| Al-Talāq (65) | **9** | ✅ |
| Nūh (71) | 4 | |
| Al-Muddaththir (74) | 2 | |
| Al-Mutaffifīn (83) | 8 | |
| Al-'Asr (103) | **6** | ✅ |
| Al-Fīl (105) | **6** | ✅ |
| **Al-Ikhlās (112)** | **3** | ✅ |

6 of 12 invariant Surahs belong to {3,6,9} = **50%** (random expectation: 33%).  
These Surahs contain none of the orthographic variant words.

---

## Part V: Orthographic Crossings — Structured, Not Random

| | K6 | Abjad |
|---|---|---|
| Differing words | 16,167 | 12,244 |
| Words crossing {3,6,9} boundary | **9,630** | **7,082** |
| Net entries | +828 | +874 |
| **p-value** | **< 0.0001** | **< 0.0001** |

**The paradox:** At word level, Uthmani adds +828 words to {3,6,9}.  
At Surah level, it removes 21 Surahs.  
Words entering {3,6,9} spread evenly across Surahs — like sugar dissolving.  
Words leaving {3,6,9} concentrate in legal Surahs — like salt changing a dish.

---

## Part VI: Bukhari Control — Same Rules, Different Text

| | Quran | Bukhari |
|---|---|---|
| Abjad net | **+874** | +167 |
| Abjad p-value | **< 0.0001 ✅** | **1.0000 ❌** |
| K6 net | +828 | +774 |
| K6 p-value | < 0.0001 | < 0.0001 |

**Same rules + same encoding + different text = reversed result (Abjad).**  
The structured crossing is a property of the Quranic text, not of the orthographic rules.  
K6 sensitivity = encoding artifact (ي≠ى in K6), not text-specific.

---

## Part VII: Letter-Merging Experiment

| System | Quran SC | Quran UT | Bukhari |
|--------|----------|----------|---------|
| Abjad (28 sounds) | z=27 ✅ | z=34 ✅ | z≈0 ❌ |
| Rasm-A (18 shapes, no dots) | z≈0 ❌ | z=0 ❌ | z=10 ✅ |
| Rasm-B (structural) | z=-6.7 ❌ | z=-1.6 ❌ | z=34 ✅ |

**Merging homographic letters destroys the Quranic fingerprint (z≈0).**  
The 28-phoneme Abjad encoding is the only system that reveals it.  
**The dots are part of the code — not decoration.**

---

## Falsified Hypotheses

| Hypothesis | Refuted by |
|-----------|-----------|
| Basmala alif shifts 113 Surahs | Basmala identical: K6=1,027,164 |
| Abjad unaffected by script | 100 Surahs change |
| Difference is marginal | 16,534 words / 7,425 unique patterns |
| Crossing is random noise | p<0.0001 both encodings |
| K6 sensitivity = text property | Bukhari also p<0.0001 in K6 — encoding artifact |
| Merging dots reveals fingerprint | Destroys it in Quran (z≈0) |

---

## Scientific Position (Option C — Full Transparency)

> "The {3,6,9} digital root fingerprint is robust at the **word level**
> (p ≈ 0) under both orthographic conventions and both encoding systems.
> At the **Surah level**, the fingerprint is sensitive to orthographic
> convention: K6=45% (p=0.011) under modern Imla'i spelling vs. 26%
> (p≈0.96) under Uthmani rasm. The difference traces to 16,534 word-level
> orthographic variants. The Basmala is identical in both scripts.
> All 10 mutawātir readings produce identical results.
> Both results are reported with full transparency."
>
> Both scripts carry the fingerprint — in different layers.  
> Imla'i (spoken form) carries it at the Surah level.  
> Uthmani (written form) carries it at the word level.  
> The difference between them is structure, not noise (p<0.0001).

---

## Reference Files

- `results/exp08_full_report.json` — all Surahs with digital roots and change direction
- `results/exp08_unified_results.json` — ten readings comparison
- `data/` — 14 recitations from tanzil.net (CC-BY 3.0)

---

*Emad Suleiman Alwan — March 22, 2026*
