# shared/utils.py

Shared utilities used by all experiments.

## Contents

| Symbol | Type | Description |
|--------|------|-------------|
| `JUMMAL_5` | dict | Classical Abjad encoding (ة=5) — used in Experiments 01–03, 06 |
| `JUMMAL_400` | dict | Abjad variant with ة=400 — not used in main experiments |
| `KHASS_6` | dict | Special-6 encoding (33 shapes, quasi-binary) — Experiments 04–07 |
| `digit_root(n)` | function | Reduce integer to 1–9 |
| `word_value(text, system)` | function | Numerical value of an Arabic word |

## The Two Systems

### Classical Abjad (JUMMAL_5)

Standard Arabic alphanumeric encoding, used since antiquity.
Letters are assigned values: ا=1, ب=2, ج=3 … غ=1000.
In this implementation, ة (tā' marbūṭa) = 5 (same as ه).

### Special-6 (KHASS_6)

An original system designed by Emad Suleiman Alwan (2026).
- Assigns values only from digits 0 and 1 (quasi-binary)
- Treats 33 distinct letter **shapes**, not 28 phonemes
- Key: ة ≠ ت (both are /t/ but have different shapes → different values)

```python
from shared.utils import JUMMAL_5, KHASS_6, digit_root, word_value

# Example
word = "بسم"
print(word_value(word, JUMMAL_5))   # 2 + 60 + 40 = 102
print(digit_root(102))              # 3
```

## Usage

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from utils import JUMMAL_5, KHASS_6, digit_root, word_value
```
