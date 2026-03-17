# Experiment 09 — Bukhari as Control Group (Gate Six)

**Date:** March 17, 2026 — Night of the 27th of Ramadan 1446H
**System:** Special-6
**Text:** Sahih al-Bukhari — 1,000 hadith | 66,349 words

---

## The Logic — Why Bukhari?

| Criterion | Quran | Bukhari |
|-----------|-------|---------|
| Language | Arabic | Arabic ✓ |
| Subject | Religious | Religious ✓ |
| About the Prophet | Yes | Yes ✓ |
| **Who drew the boundaries** | **God** | **Imam al-Bukhari** |

**The only variable: who divided the text.**
If Quran is significant and Bukhari is not → the difference is in divine division, not in language or subject matter.

---

## Methodology

| Element | Details |
|---------|---------|
| System | Special-6 (KHASS_6 from utils.py) |
| File structure | Each line = one hadith |
| Natural unit | The hadith (1,000 hadith) |
| Analogue to Quran verse | The hadith = smallest natural unit |

---

## Results (Permutation Test | March 17, 2026)

| Division | Units | {3,6,9} | Pct | p-value |
|----------|-------|---------|-----|---------|
| A: Natural hadith | 1,000 | 350 | 35.0% | 0.1390 ✗ |
| B: Equal (~66 words) | 1,000 | 350 | 35.0% | 0.1348 ✗ |
| C: Random (median/1,000) | 1,000 | 333 | 33.3% | — |
| D: Quran's Surah lengths | 114 | 39 | 34.2% | 0.4542 ✗ |

### Test C — Distribution Over 1,000 Random Divisions

```
median=333 | 95th percentile=358
Natural hadith (350) at 87th percentile — not exceptional
```

---

## Direct Comparison — Quran vs Bukhari

```
Variable: who drew the boundaries
────────────────────────────────────────────────────────────
Who divided    Text            Division         Result
────────────────────────────────────────────────────────────
Divine         Quran — Surahs  real sizes       p=0.007  ✅
Divine         Quran — verses  natural          p=0.010  ✅
Human          Bukhari         natural hadith   p=0.139  ✗
Human          Bukhari         equal chunks     p=0.135  ✗
Human          Bukhari         random           —        ✗ (87th pct)
Human          Bukhari         Quran's sizes    p=0.454  ✗
```

---

## Verdict — Gate Six

**Bukhari shows no fingerprint under any division.**

Natural division (Imam al-Bukhari's own hadith structure) = **p=0.139** — not significant.
Not with equal chunks. Not with random sizes. Not with Quran's Surah lengths imposed on it.

> **The property belongs to the Quran alone.**
> Not a property of the Arabic language.
> Not a property of religious text.
> Not a property of text about the Prophet.
> **The only difference: who drew the boundaries.**

---

## The Complete Picture — After 9 Experiments

```
Level                         Verdict    p-value    Text
──────────────────────────────────────────────────────────────
Quranic verse                 ✅          0.010     Quran
Surah — divine division       ✅          0.007     Quran   ← peak
Surah — equal chunks          ✗           0.137     Quran
Surah — random                ✗           —         Quran (99th pct)
Bukhari hadith — natural      ✗           0.139     Bukhari
Bukhari hadith — equal        ✗           0.135     Bukhari
Bukhari — Quran's sizes       ✗           0.454     Bukhari
```

---

## Next Step — Gate Seven

Test a revealed text with its own natural structure:
- **Torah in Arabic**: Does the property extend to other revealed texts?
- **Bible in Arabic**: Broader Semitic comparison
- Question: Is the fingerprint unique to the Quran — or shared by all revealed texts?
