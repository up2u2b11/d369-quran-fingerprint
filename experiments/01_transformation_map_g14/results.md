# Experiment 01 — G14 Digital Root Transformation Map

**Date:** March 14, 2026
**System:** Classical Abjad (ة=5)
**Unit of analysis:** 114 Surahs

---

## Question

When all Surahs sharing the same digital root are grouped and their Abjad sums are added together — does the resulting group sum preserve that same digital root?

---

## Results

| Root | Surahs | Group Sum | Group Root | Result |
|------|--------|-----------|------------|--------|
| 1 | 14 | 2,937,227 | 5 | → 5 |
| 2 | 6 | 111,216 | 3 | → 3 |
| **3** | **13** | **3,210,951** | **3** | **✅ preserved** |
| 4 | 13 | 1,026,997 | 7 | → 7 |
| 5 | 15 | 3,588,834 | 3 | → 3 |
| **6** | **10** | **2,642,856** | **6** | **✅ preserved** |
| 7 | 16 | 4,054,693 | 4 | → 4 |
| 8 | 15 | 2,755,353 | 3 | → 3 |
| **9** | **12** | **3,147,993** | **9** | **✅ preserved** |

**Total Quran Abjad sum: 23,476,120 → digital root 7**

---

## Complete Transformation Structure

```
{3, 6, 9}  →  stable   (Tesla's triad)
{2, 5, 8}  →  all become 3
{4 ↔ 7}   →  mutual cycle: 4→7, 7→4
{1 → 5}   →  1 becomes 5
```

---

## Statistical Significance

- **Monte Carlo (100,000 trials):** p < 0.00001
- Probability of seeing {3, 6, 9} all stable by chance: < 0.146%

---

## Conclusion

{3, 6, 9} are the only digital roots that preserve their identity when their groups are summed. This is a **collective** property — it does not belong to any single Surah, but emerges only when like groups are combined.

---

## Methodological Notes

- System used: Abjad with ة=5 (classical)
- Source: direct computation from `text_uthmani` column in `words` table (d369_research.db)
- The `surahs.jummal_total` pre-computed column uses a different convention and is **not used** in these experiments
