# Data Files

## d369_research.db

SQLite database containing the `words` table — 78,248 Quranic words.

### Schema

| Column | Type | Description |
|--------|------|-------------|
| `word_id` | INTEGER | Word identifier |
| `surah_id` | INTEGER | Surah number (1–114) |
| `ayah_number` | INTEGER | Verse number |
| `word_position` | INTEGER | Position within the verse |
| `word_pos_in_quran` | INTEGER | Absolute position in the Quran |
| `text_uthmani` | TEXT | Uthmanic script with full diacritics |
| `text_clean` | TEXT | Simplified text |
| `jummal_value` | INTEGER | Classical Abjad value (ة=5) |
| `digit_root` | INTEGER | Digital root of the Abjad value |
| `jummal_special_6` | TEXT | Special-6 value |

### Quick Start

```python
import sqlite3
conn = sqlite3.connect("data/d369_research.db")
c = conn.cursor()

# First 5 words
c.execute("SELECT text_clean, jummal_value, jummal_special_6 FROM words LIMIT 5")
for row in c.fetchall():
    print(row)
```

### Important Note

**Do not use `surahs.jummal_total` if present.** That column uses a slightly
different convention. All experiments in this repository compute Abjad sums
directly from `text_uthmani` in the `words` table to ensure consistency.

---

## Comparative Texts

| File | Source | Size |
|------|--------|------|
| `quran_simple.txt` | Quran — simplified script | ~1.3 MB |
| `bukhari_sample.txt` | Sahih al-Bukhari — sample | ~1.0 MB |
| `futuhat_v1.txt` | Ibn Arabi's Futuhat — Vol. 1 | ~1.8 MB |
| `muallaqat.txt` | The Seven Mu'allaqat (pre-Islamic poetry) | ~7 KB |

These texts are used as controls in Experiments 03, 04, and 07.

### Setting paths

```python
import os
os.environ["D369_DB"]   = "data/d369_research.db"
os.environ["D369_DATA"] = "data/"
```
