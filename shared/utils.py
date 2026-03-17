"""
shared/utils.py — Core utilities for d369 experiments
======================================================

Contains:
  - JUMMAL_5     : Classical Abjad dictionary (ة=5)
  - JUMMAL_400   : Abjad with ة=400 (not used in main experiments)
  - KHASS_6      : Special-6 encoding — original system by Emad Suleiman Alwan
  - digit_root() : Reduce any integer to a single digit 1–9
  - word_value() : Compute the numerical value of an Arabic word

Intellectual property: Emad Suleiman Alwan — up2b.ai — 2026
"""

# ──────────────────────────────────────────────────────────────
# Classical Abjad (ة=5) — the standard used in all main experiments
# ──────────────────────────────────────────────────────────────
JUMMAL_5: dict = {
    "ا": 1,  "أ": 1,  "إ": 1,  "آ": 1,  "ٱ": 1,
    "ب": 2,
    "ج": 3,
    "د": 4,
    "ه": 5,  "ة": 5,
    "و": 6,  "ؤ": 6,
    "ز": 7,
    "ح": 8,
    "ط": 9,
    "ي": 10, "ى": 10, "ئ": 10,
    "ك": 20,
    "ل": 30,
    "م": 40,
    "ن": 50,
    "س": 60,
    "ع": 70,
    "ف": 80,
    "ص": 90,
    "ق": 100,
    "ر": 200,
    "ش": 300,
    "ت": 400, "ث": 400,
    "خ": 600,
    "ذ": 700,
    "ض": 800,
    "ظ": 900,
    "غ": 1000,
}

# Abjad with ة=400 (alternative — not used in main G14 experiment)
JUMMAL_400: dict = dict(JUMMAL_5)
JUMMAL_400["ة"] = 400

# ──────────────────────────────────────────────────────────────
# Special-6 Encoding — Original system by Emad Suleiman Alwan
#
# Assigns a unique quasi-binary value to each of the 33 distinct
# Arabic letter SHAPES (not 28 phonemes).
#
# Key distinction from Abjad:
#   ة ≠ ت  (11 vs 100)
#   ؤ ≠ و  (1000000 vs 111110)
#   ئ ≠ ي  (1000001 vs 111000)
#
# The values follow a semi-binary pattern: each phonetic group
# receives a number built from 0s and 1s, assigned in ascending
# order of complexity.
# ──────────────────────────────────────────────────────────────
KHASS_6: dict = {
    "أ": 1,      "إ": 1,    "آ": 1,    "ٱ": 1,    "ا": 1,
    "ب": 10,
    "ة": 11,
    "ت": 100,
    "ث": 101,
    "ج": 111,
    "ح": 110,
    "خ": 1000,
    "د": 1001,
    "ذ": 1011,
    "ر": 1111,
    "ز": 1100,
    "س": 1110,
    "ش": 10000,
    "ص": 10001,
    "ض": 10011,
    "ط": 10111,
    "ظ": 11111,
    "ع": 11110,
    "غ": 11100,
    "ف": 11000,
    "ق": 100000,
    "ك": 100001,
    "ل": 100011,
    "م": 100111,
    "ن": 101111,
    "ه": 111111,
    "و": 111110,
    "ؤ": 1000000,
    "ى": 111100,
    "ي": 111000,
    "ئ": 1000001,
    "ء": 110000,
}


def digit_root(n: int) -> int:
    """
    Reduce a positive integer to a single digit 1–9.
    digit_root(0) = 0
    digit_root(18) = 9
    digit_root(19) = 1

    Formula: 1 + (n - 1) % 9  for n > 0
    """
    if n <= 0:
        return 0
    return 1 + (n - 1) % 9


def word_value(text: str, system: dict) -> int:
    """
    Compute the numerical value of an Arabic word using a given encoding system.

    Args:
        text   : Arabic text (word or phrase, diacritics are ignored)
        system : One of JUMMAL_5, JUMMAL_400, KHASS_6

    Returns:
        Sum of letter values (0 if no recognized letters found)
    """
    return sum(system.get(ch, 0) for ch in text)
