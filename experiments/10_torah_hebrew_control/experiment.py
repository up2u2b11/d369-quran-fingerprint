"""
Experiment 10 — Torah (Hebrew) as Control Group (Gate Seven)
=============================================================
Question: Is the {3,6,9} fingerprint unique to the Quran — or
          shared by other revealed texts?

Logic: Torah is:
  - A revealed text (divine origin claimed)
  - Analyzed in its ORIGINAL LANGUAGE (Hebrew, not a translation)
  - Using the Hebrew equivalent of Abjad: Gematria (א=1...ת=400)
  - Divided by its OWN natural units (Parashot — 54 sections)
       → analogous to Surahs in the Quran

Comparison:
  Quran   — Arabic   — Gematria-equivalent (KHASS_6) — Surahs (114)  → p=0.007 ✅
  Torah   — Hebrew   — Gematria                      — Parashot (54) → ?

File structure:
  torah_hebrew.jsonl  — 5,846 verses | 69,196 words
  parashot_boundaries.json — 54 Parashot with exact (book, chapter, verse) boundaries

Tests (same 4-battery as Experiments 08 and 09):
  A — Natural Parasha units (54 Parashot — traditional Jewish structure)
  B — Equal division (54 × ~1,281 words)
  C — Random division × 1,000 (distribution benchmark)
  D — Torah split using Quran's Surah lengths (114 units, direct comparison)

Intellectual property: Emad Suleiman Alwan — March 17, 2026
"""

import json
import random
import re
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import digit_root

DATA_DIR = os.environ.get("D369_DATA", "/root/d369/data")
TORAH_PATH      = os.path.join(DATA_DIR, "torah_hebrew.jsonl")
PARASHOT_PATH   = os.path.join(DATA_DIR, "parashot_boundaries.json")

# ── Hebrew Gematria (Standard / Mispar Hechrachi) ───────────────────────────
# The Hebrew equivalent of Arabic Abjad.
# Each letter maps to its classical numerical value.
# Sofit (final) forms carry the same value as their base form.
GEMATRIA = {
    'א':1,  'ב':2,  'ג':3,  'ד':4,  'ה':5,  'ו':6,  'ז':7,  'ח':8,  'ט':9,
    'י':10, 'כ':20, 'ך':20, 'ל':30, 'מ':40, 'ם':40, 'נ':50, 'ן':50,
    'ס':60, 'ע':70, 'פ':80, 'ף':80, 'צ':90, 'ץ':90,
    'ק':100,'ר':200,'ש':300,'ת':400,
}


def clean_hebrew(word: str) -> str:
    """Strip vowel points and cantillation marks — keep only base letters."""
    return re.sub(r'[^\u05d0-\u05ea]', '', word)


def gematria_value(word: str) -> int:
    return sum(GEMATRIA.get(ch, 0) for ch in clean_hebrew(word))


def load_torah(path: str) -> tuple:
    """
    Load Torah from JSONL. Each line: {"book":int, "chapter":int, "verse":int, "words":[...]}
    Returns:
      verses  — list of (book, chapter, verse, word_vals)
      all_vals — flat list of all gematria values
    """
    verses = []
    all_vals = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            rec = json.loads(line.strip())
            vals = [gematria_value(w) for w in rec['words'] if clean_hebrew(w)]
            if vals:
                verses.append((rec['book'], rec['chapter'], rec['verse'], vals))
                all_vals.extend(vals)
    return verses, all_vals


def load_parashot(path: str) -> list:
    """Load 54 Parasha boundaries: [[name, book, chapter, verse], ...]"""
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def build_parasha_sizes(verses: list, parashot: list) -> list:
    """
    Compute word count of each Parasha.
    A Parasha starts at (book, chapter, verse) and ends just before the next one.
    """
    # Build index: (book, chapter, verse) → flat verse index
    verse_index = {(b, c, v): i for i, (b, c, v, _) in enumerate(verses)}

    # Build start positions in flat word list
    word_starts = []
    pos = 0
    for (b, c, v, vals) in verses:
        word_starts.append(pos)
        pos += len(vals)
    total_words = pos

    parasha_word_starts = []
    for (name, book, chapter, verse) in parashot:
        key = (book, chapter, verse)
        if key in verse_index:
            vi = verse_index[key]
            parasha_word_starts.append(word_starts[vi])

    sizes = []
    for i, start in enumerate(parasha_word_starts):
        end = parasha_word_starts[i+1] if i+1 < len(parasha_word_starts) else total_words
        sizes.append(end - start)

    return sizes


def count_369(vals: list, sizes: list) -> int:
    idx = count = 0
    for sz in sizes:
        if digit_root(sum(vals[idx:idx+sz])) in (3, 6, 9):
            count += 1
        idx += sz
    return count


def count_369_wrap(vals: list, sizes: list) -> int:
    """Cyclic wrap for Test D (Quran sizes applied to Torah)."""
    n = len(vals)
    idx = count = 0
    for sz in sizes:
        chunk = [vals[(idx + i) % n] for i in range(sz)]
        if digit_root(sum(chunk)) in (3, 6, 9):
            count += 1
        idx = (idx + sz) % n
    return count


def perm_test(vals: list, sizes: list, observed: int, trials: int = 10_000) -> float:
    v = vals.copy()
    exceed = 0
    for _ in range(trials):
        random.shuffle(v)
        if count_369(v, sizes) >= observed:
            exceed += 1
    return exceed / trials


def perm_test_wrap(vals: list, sizes: list, observed: int, trials: int = 5_000) -> float:
    v = vals.copy()
    exceed = 0
    for _ in range(trials):
        random.shuffle(v)
        if count_369_wrap(v, sizes) >= observed:
            exceed += 1
    return exceed / trials


def random_dist(vals: list, n_units: int, trials: int = 1_000) -> list:
    N = len(vals)
    counts = []
    for _ in range(trials):
        cuts = sorted(random.sample(range(1, N), n_units - 1))
        sizes = ([cuts[0]]
                 + [cuts[i] - cuts[i-1] for i in range(1, n_units - 1)]
                 + [N - cuts[-1]])
        counts.append(count_369(vals, sizes))
    counts.sort()
    return counts


def load_quran_surah_sizes(db_path: str) -> list:
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM words GROUP BY surah_id ORDER BY surah_id")
    sizes = [r[0] for r in c.fetchall()]
    conn.close()
    return sizes


def run(torah_path: str = TORAH_PATH, parashot_path: str = PARASHOT_PATH) -> dict:
    DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")

    print("=" * 65)
    print("Experiment 10 — Torah (Hebrew) as Revealed-Text Control")
    print("Gate Seven: Does the fingerprint extend beyond the Quran?")
    print("=" * 65)
    print("\nLogic:")
    print("  Torah = Revealed ✓ | Original language (Hebrew) ✓")
    print("  Gematria = Hebrew Abjad equivalent ✓")
    print("  Parashot = Torah's own natural divisions ✓")
    print("  Question: Does divine division produce {3,6,9} in Torah too?")

    verses, all_vals = load_torah(torah_path)
    parashot = load_parashot(parashot_path)
    parasha_sizes = build_parasha_sizes(verses, parashot)

    N = len(all_vals)
    n_para = len(parasha_sizes)
    n_verses = len(verses)

    print(f"\nTorah: {N:,} words | {n_verses:,} verses | {n_para} Parashot")
    print(f"System: Gematria (Hebrew Abjad equivalent)")
    print(f"Method: same 4-battery as Experiments 08 and 09")

    # Test A — Natural Parasha units
    print(f"\n{'─'*55}")
    print(f"Test A — Natural Parashot ({n_para} — traditional Jewish structure)")
    obs_A = count_369(all_vals, parasha_sizes)
    print(f"   {{3,6,9}} = {obs_A}/{n_para} = {obs_A/n_para*100:.1f}%  — permutation test (10,000)...")
    p_A = perm_test(all_vals, parasha_sizes, obs_A, 10_000)
    print(f"   p = {p_A:.4f}  {'✅ significant' if p_A<0.05 else '✗ not significant'}")

    # Test B — Equal division
    print(f"\n{'─'*55}")
    chunk = N // n_para
    equal_sizes = [chunk] * (n_para - 1) + [N - chunk * (n_para - 1)]
    print(f"Test B — Equal division ({n_para} × ~{chunk:,} words)")
    obs_B = count_369(all_vals, equal_sizes)
    print(f"   {{3,6,9}} = {obs_B}/{n_para} = {obs_B/n_para*100:.1f}%  — permutation test (5,000)...")
    p_B = perm_test(all_vals, equal_sizes, obs_B, 5_000)
    print(f"   p = {p_B:.4f}  {'✅ significant' if p_B<0.05 else '✗ not significant'}")

    # Test C — Random × 1,000
    print(f"\n{'─'*55}")
    print(f"Test C — Random division × 1,000 ({n_para} units)")
    rand_counts = random_dist(all_vals, n_para, 1_000)
    median_C = rand_counts[500]
    pct_A    = sum(1 for x in rand_counts if x < obs_A) / 10
    thr95    = rand_counts[950]
    print(f"   Median:          {median_C}/{n_para} = {median_C/n_para*100:.1f}%")
    print(f"   95th percentile: {thr95}/{n_para}")
    print(f"   Natural Parashot ({obs_A}) at {pct_A:.1f}th percentile — {'exceptional' if pct_A>=95 else 'not exceptional'}")

    # Test D — Torah with Quran's Surah lengths
    print(f"\n{'─'*55}")
    print("Test D — Torah split using Quran's Surah lengths (114 units)")
    try:
        surah_sizes = load_quran_surah_sizes(DB_PATH)
        obs_D = count_369_wrap(all_vals, surah_sizes)
        print(f"   {{3,6,9}} = {obs_D}/114 = {obs_D/114*100:.1f}%  — permutation test (5,000)...")
        p_D = perm_test_wrap(all_vals, surah_sizes, obs_D, 5_000)
        print(f"   p = {p_D:.4f}  {'✅ significant' if p_D<0.05 else '✗ not significant'}")
    except Exception as e:
        print(f"   (Database not available — skipped: {e})")
        obs_D = p_D = None

    # Summary
    print(f"\n{'='*65}")
    print(f"{'Division':<32} {'Units':>6} {'{3,6,9}':>8} {'Pct':>7} {'p-value':>10}")
    print("─" * 65)
    print(f"  {'A: Natural Parashot':<30} {n_para:>6} {obs_A:>8} {obs_A/n_para*100:>6.1f}% {p_A:>10.4f}  {'✅' if p_A<0.05 else '✗'}")
    print(f"  {'B: Equal (~1,281 words)':<30} {n_para:>6} {obs_B:>8} {obs_B/n_para*100:>6.1f}% {p_B:>10.4f}  {'✅' if p_B<0.05 else '✗'}")
    print(f"  {'C: Random (median)':<30} {n_para:>6} {median_C:>8} {median_C/n_para*100:>6.1f}% {'—':>10}  ({obs_A} at {pct_A:.0f}th pct)")
    if obs_D is not None:
        print(f"  {'D: Quran Surah lengths':<30} {114:>6} {obs_D:>8} {obs_D/114*100:>6.1f}% {p_D:>10.4f}  {'✅' if p_D<0.05 else '✗'}")
    print("=" * 65)

    print("\nComparison — Quran vs Torah:")
    print(f"  Quran — Surahs (divine division): 51/114 = 44.7%  p=0.007  ✅")
    print(f"  Quran — Verses (natural):       2164/6236 = 34.7%  p=0.010  ✅")
    print(f"  Torah — Parashot (natural):        {obs_A}/{n_para} = {obs_A/n_para*100:.1f}%  p={p_A:.3f}  {'✅' if p_A<0.05 else '✗'}")

    print("\nVerdict:")
    if p_A >= 0.05 and p_B >= 0.05:
        print("→ Torah shows no {3,6,9} fingerprint under any division")
        print("  The property does not extend to the Torah")
        print("  The fingerprint belongs to the Quran alone — even among revealed texts")
    elif p_A < 0.05:
        print("→ Torah shows a fingerprint in its natural Parasha division")
        print("  The property may extend to other revealed texts")
    else:
        print("→ Mixed result — requires deeper analysis")

    result = {
        "A": {"obs": obs_A, "n": n_para, "p": p_A},
        "B": {"obs": obs_B, "n": n_para, "p": p_B},
        "C": {"median": median_C, "percentile_A": pct_A, "threshold_95": thr95},
    }
    if obs_D is not None:
        result["D"] = {"obs": obs_D, "n": 114, "p": p_D}
    return result


if __name__ == "__main__":
    run()
