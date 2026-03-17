# Experiment 06 — Transformation Maps: Abjad vs Special-6

**Date:** March 17, 2026
**Systems:** Classical Abjad (ة=5) + Special-6
**Unit of analysis:** 114 Surahs grouped by digital root (9 groups)

---

## Results

### Abjad (G14) — the original map

| Root | Surahs | Group Sum | → Root | Result |
|------|--------|-----------|--------|--------|
| 1 | 14 | 2,937,227 | 5 | → 5 |
| 2 | 6 | 111,216 | 3 | → 3 |
| **3** | **13** | **3,210,951** | **3** | **✅ stable** |
| 4 | 13 | 1,026,997 | 7 | → 7 |
| 5 | 15 | 3,588,834 | 3 | → 3 |
| **6** | **10** | **2,642,856** | **6** | **✅ stable** |
| 7 | 16 | 4,054,693 | 4 | → 4 |
| 8 | 15 | 2,755,353 | 3 | → 3 |
| **9** | **12** | **3,147,993** | **9** | **✅ stable** |

**Stable under Abjad: {3, 6, 9}**

---

### Special-6 — its own map

| Root | Surahs | → Root | Result |
|------|--------|--------|--------|
| 1 | 11 | 2 | → 2 |
| 2 | 9 | 9 | → 9 |
| 3 | 15 | 9 | → 9 |
| 4 | 15 | 6 | → 6 |
| 5 | 8 | 4 | → 4 |
| 6 | 18 | 9 | → 9 |
| 7 | 9 | 9 | → 9 |
| 8 | 11 | 7 | → 7 |
| **9** | **18** | **9** | **✅ stable** |

**Stable under Special-6: {9} only**

---

## Comparison

| Root | Abjad result | Special-6 result | Match? |
|------|-------------|-----------------|--------|
| 1 | 1→5 | 1→2 | ✗ |
| 2 | 2→3 | 2→9 | ✗ |
| 3 | 3→3 | 3→9 | ✗ |
| 4 | 4→7 | 4→6 | ✗ |
| 5 | 5→3 | 5→4 | ✗ |
| 6 | 6→6 | 6→9 | ✗ |
| 7 | 7→4 | 7→9 | ✗ |
| 8 | 8→3 | 8→7 | ✗ |
| **9** | **9→9** | **9→9** | **✅** |

**Overlap: 1/9** — only {9} is shared

---

## Conclusion

```
Abjad    → sees {3, 6, 9} stability in the transformation map
Special-6 → sees {9} stability in the map, but {3, 6, 9} in the Surah-level count (Exp. 04)

Common ground: {9} is present across all tests and both systems.
```

---

## Open Question

Under Special-6, nearly all groups converge to 9. Is this because Special-6 values are much larger (reaching billions), making root-9 statistically more likely? Or is {9} a genuine structural property of this text?

→ **Experiment 07** partially answers this: the shuffled Quran and Bukhari do not show the same pattern, suggesting the convergence is text-specific, not a mathematical artifact of large numbers.
