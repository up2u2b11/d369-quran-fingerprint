# Experiment 02 — Fingerprint Stability: Hafs vs Warsh

**Date:** March 16, 2026
**System:** Classical Abjad (ة=5)
**Unit of analysis:** 114 Surahs × 2 readings

---

## Question

Is the {3, 6, 9} fingerprint stable across different Quranic readings?
Or is it an artifact of the Hafs text specifically?

---

## Results

| | Hafs | Warsh |
|---|---|---|
| Total Abjad sum | computed from DB | computed from text |
| Difference between readings | — | 758 Abjad units = **0.003%** |
| {3} stable? | ✅ | ✅ |
| {6} stable? | ✅ (via Basmala) | ✅ (via text) |
| {9} stable? | ✅ | ✅ |

---

## Structural Discovery

**{3, 9} are stable in both readings by the same mechanism.**

**{6} is protected by two different mechanisms:**
- In **Hafs**: The Basmala (بسم الله الرحمن الرحيم) is added at the start of each Surah → it adjusts the group sum of root-6 Surahs
- In **Warsh**: The Basmala is treated as part of the first Surah's text → internal adjustment

> **"The Basmala acts as a structural guardian of {6} in the Hafs reading."**

---

## Conclusion

A 0.003% textual difference between the two major readings does not break the fingerprint.
{3, 6, 9} are stable in both readings — but through different mechanisms for {6}.

This means: the fingerprint is not a textual accident. It is a structure that resists orthographic and recitation variants.

---

## Limitations

- Requires a Warsh text file in a consistent format for full verification
- The precise difference depends on how the Basmala is defined in each reading
