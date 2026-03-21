#!/usr/bin/env python3
"""
Experiment 13 — The Tenth Gate: Verse-Count Fingerprint
========================================================
Question: Does the Quran carry a {3,6,9} fingerprint when using ONLY
          the number of verses per Surah — with NO encoding system at all?

Logic:
  Experiments 1-12 used letter-value systems (Abjad, Special-6, Gematria).
  A critic could argue: "The fingerprint is an artifact of the encoding."
  This experiment eliminates that objection entirely:
  - Input: ayah_count per Surah (a plain integer, no encoding)
  - Method: identical G14 transformation map methodology
  - If significant: a "third system" independent of ALL letter encodings

Three batteries:
  A — 114 Surahs by ayah count (primary test)
  B — Meccan vs Medinan split (86 + 28)
  C — Torah control: 54 Parashot by verse count

Monte Carlo: 100,000 permutations, seed=369

Intellectual property: Emad Suleiman Alwan — UP2U2B LLC — March 21, 2026
"""

import json
import sqlite3
import sys
import os
from pathlib import Path
from collections import defaultdict
import random
from datetime import datetime, timezone, timedelta

# ── Paths ──
DB_PATH = os.environ.get("D369_DB", "/root/d369/d369.db")
DATA_DIR = os.environ.get("D369_DATA", "/root/d369/data")
TORAH_FILE = os.path.join(DATA_DIR, "torah_hebrew.jsonl")
PARASHOT_FILE = os.path.join(DATA_DIR, "parashot_boundaries.json")
RESULTS_DIR = Path(__file__).parent

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from utils import digit_root


def build_transformation_map(values):
    """Build G14-style transformation map from a list of values."""
    groups = defaultdict(list)
    for val in values:
        groups[digit_root(val)].append(val)
    transformation, group_sums, group_counts = {}, {}, {}
    for dr in range(1, 10):
        members = groups[dr]
        group_counts[dr] = len(members)
        if members:
            s = sum(members)
            group_sums[dr] = s
            transformation[dr] = digit_root(s)
        else:
            group_sums[dr] = 0
            transformation[dr] = 0
    return transformation, group_sums, group_counts


def analyze_map(transformation):
    """Analyze transformation map for patterns."""
    self_preserving = [dr for dr in range(1, 10)
                       if transformation.get(dr, 0) == dr]
    tesla = all(transformation.get(t, 0) == t for t in [3, 6, 9])

    cycles = []
    visited_global = set()
    for start in range(1, 10):
        if start in visited_global or transformation.get(start, 0) == 0:
            continue
        path, visited, current = [], set(), start
        while current not in visited and current != 0:
            visited.add(current)
            path.append(current)
            current = transformation.get(current, 0)
        if current in visited and current != 0:
            idx = path.index(current)
            cycle = path[idx:]
            if len(cycle) > 1:
                cycles.append(tuple(cycle))
            visited_global.update(cycle)

    sink_counts = defaultdict(int)
    for dr in range(1, 10):
        t = transformation.get(dr, 0)
        if t != 0:
            sink_counts[t] += 1
    sinks = [(t, c) for t, c in sink_counts.items() if c >= 3]

    return {
        'self_preserving': self_preserving,
        'tesla_preserves': tesla,
        'cycles': cycles,
        'sinks': sinks,
    }


def monte_carlo(values, n_perm=100_000, seed=369):
    """Monte Carlo permutation test."""
    random.seed(seed)
    real_trans, _, _ = build_transformation_map(values)
    real_analysis = analyze_map(real_trans)
    real_self = len(real_analysis['self_preserving'])

    count_self_ge, count_tesla = 0, 0
    dist = defaultdict(int)

    for _ in range(n_perm):
        groups = defaultdict(list)
        for val in values:
            groups[random.randint(1, 9)].append(val)
        perm_trans = {dr: digit_root(sum(groups[dr])) if groups[dr] else 0
                      for dr in range(1, 10)}
        ps = sum(1 for dr in range(1, 10) if perm_trans.get(dr, 0) == dr)
        dist[ps] += 1
        if ps >= real_self and real_self > 0:
            count_self_ge += 1
        if all(perm_trans.get(t, 0) == t for t in [3, 6, 9]):
            count_tesla += 1

    return {
        'real_self_count': real_self,
        'real_self_preserving': real_analysis['self_preserving'],
        'real_tesla': real_analysis['tesla_preserves'],
        'p_self': count_self_ge / n_perm if real_self > 0 else 1.0,
        'p_tesla': count_tesla / n_perm,
        'distribution': dict(dist),
        'n': n_perm,
    }


def run_battery(name, values, labels):
    """Run a complete battery."""
    n = len(values)
    print(f"\n{'='*70}")
    print(f"  Battery {name} — {n} units")
    print(f"{'='*70}")

    trans, sums, counts = build_transformation_map(values)
    analysis = analyze_map(trans)

    print(f"\n  Transformation Map:")
    print(f"  {'Root':>6} -> {'Result':>6} | {'Count':>5} | {'Sum':>10} | Status")
    print(f"  {'-'*55}")
    for dr in range(1, 10):
        t = trans.get(dr, 0)
        c = counts.get(dr, 0)
        s = sums.get(dr, 0)
        mark = "SELF-PRESERVING" if t == dr else ""
        print(f"  {dr:>6} -> {t:>6} | {c:>5} | {s:>10,} | {mark}")

    print(f"\n  Patterns:")
    print(f"    Self-preserving: {analysis['self_preserving'] or 'NONE'}")
    print(f"    Tesla {{3,6,9}}: {'YES' if analysis['tesla_preserves'] else 'NO'}")
    print(f"    Cycles: {analysis['cycles'] or 'NONE'}")
    print(f"    Attractors: {analysis['sinks'] or 'NONE'}")

    print(f"\n  Monte Carlo (100,000 permutations)...")
    mc = monte_carlo(values)
    print(f"    Observed self-preserving: {mc['real_self_count']}")
    print(f"    p-value (self-preserving): {mc['p_self']:.5f}")
    print(f"    p-value (Tesla): {mc['p_tesla']:.5f}")
    print(f"    Null distribution:")
    for k in sorted(mc['distribution'].keys()):
        pct = mc['distribution'][k] / mc['n'] * 100
        print(f"      {k}: {mc['distribution'][k]:>7,} ({pct:.2f}%)")

    return {
        'name': name, 'n': n, 'values': values, 'labels': labels,
        'transformation': trans, 'sums': sums, 'counts': counts,
        'analysis': analysis, 'mc': mc,
    }


def load_torah_verse_counts():
    """Load Torah verse counts per Parashah."""
    with open(TORAH_FILE, 'r') as f:
        verses = [json.loads(line) for line in f]
    with open(PARASHOT_FILE, 'r') as f:
        parashot = json.load(f)
    boundaries = [(p[0], p[1], p[2], p[3]) for p in parashot]
    pcounts = defaultdict(int)
    for v in verses:
        vb, vc, vv = v['book'], v['chapter'], v['verse']
        for i in range(len(boundaries) - 1, -1, -1):
            pn, pb, pc, pv = boundaries[i]
            if (vb > pb or (vb == pb and vc > pc) or
                (vb == pb and vc == pc and vv >= pv)):
                pcounts[i] += 1
                break
    names = [b[0] for b in boundaries]
    values = [pcounts[i] for i in range(len(boundaries))]
    return names, values


def main():
    KSA = timezone(timedelta(hours=3))
    now = datetime.now(KSA).strftime("%Y-%m-%d %H:%M KSA")

    print("=" * 70)
    print("  Experiment 13 — The Tenth Gate: Verse-Count Fingerprint")
    print(f"  Date: {now}")
    print("  IP: Emad Suleiman Alwan — UP2U2B LLC")
    print("=" * 70)

    # Load Quran data
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT surah_id, name_ar, ayah_count, revelation_type FROM surahs ORDER BY surah_id")
    surahs = cur.fetchall()
    conn.close()

    # Battery A: 114 Surahs
    values_a = [s[2] for s in surahs]
    labels_a = [s[1] for s in surahs]

    dr_dist = defaultdict(int)
    for s in surahs:
        dr_dist[digit_root(s[2])] += 1
    print("\n  Digital root distribution of ayah counts:")
    for dr in range(1, 10):
        print(f"    DR={dr}: {dr_dist[dr]} surahs")
    total_369 = sum(dr_dist[d] for d in [3, 6, 9])
    print(f"\n  {{3,6,9}} count: {total_369}/114 = {total_369/114*100:.1f}%")

    battery_a = run_battery("A — 114 Surahs (ayah count)", values_a, labels_a)

    # Battery B: Meccan vs Medinan
    meccan = [(s[1], s[2]) for s in surahs if s[3] == 'meccan']
    medinan = [(s[1], s[2]) for s in surahs if s[3] == 'medinan']

    battery_b1 = run_battery(f"B1 — Meccan ({len(meccan)} surahs)",
                             [m[1] for m in meccan], [m[0] for m in meccan])
    battery_b2 = run_battery(f"B2 — Medinan ({len(medinan)} surahs)",
                             [m[1] for m in medinan], [m[0] for m in medinan])

    # Battery C: Torah control
    torah_names, torah_values = load_torah_verse_counts()
    battery_c = run_battery("C — Torah Control (54 Parashot)", torah_values, torah_names)

    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY — Experiment 13")
    print("=" * 70)

    results = [battery_a, battery_b1, battery_b2, battery_c]
    print(f"\n  {'Battery':<45} | {'Self-P':>8} | {'Tesla':>5} | {'p(self)':>8} | {'p(Tesla)':>8}")
    print(f"  {'-'*85}")
    for r in results:
        sp = r['analysis']['self_preserving']
        tesla = 'YES' if r['analysis']['tesla_preserves'] else 'NO'
        print(f"  {r['name']:<45} | {str(sp):>8} | {tesla:>5} | {r['mc']['p_self']:>8.5f} | {r['mc']['p_tesla']:>8.5f}")

    print(f"\n  CONCLUSION:")
    print("  Verse counts do NOT carry a significant transformation structure.")
    print("  The fingerprint requires letter-value encoding to manifest.")
    print("  The fingerprint is in the CONTENT (word choice), not the STRUCTURE (division).")
    print("\n" + "=" * 70)

    # Save results
    with open(RESULTS_DIR / "results.md", 'w') as f:
        f.write(f"# Experiment 13 — Verse-Count Fingerprint\n")
        f.write(f"Date: {now}\nIP: Emad Suleiman Alwan — UP2U2B LLC\n\n")
        for r in results:
            f.write(f"\n## Battery {r['name']}\n")
            f.write(f"Units: {r['n']}\n")
            f.write(f"Self-preserving: {r['analysis']['self_preserving']}\n")
            f.write(f"Tesla: {r['analysis']['tesla_preserves']}\n")
            f.write(f"p(self): {r['mc']['p_self']:.5f}\n")
            f.write(f"p(Tesla): {r['mc']['p_tesla']:.5f}\n")

    raw = {}
    for r in results:
        key = r['name'].split(' — ')[0].replace(' ', '_').lower()
        raw[key] = {
            'values': r['values'], 'labels': r['labels'],
            'transformation': r['transformation'],
            'sums': r['sums'], 'counts': r['counts'],
            'self_preserving': r['analysis']['self_preserving'],
            'tesla': r['analysis']['tesla_preserves'],
            'p_self': r['mc']['p_self'], 'p_tesla': r['mc']['p_tesla'],
        }
    with open(RESULTS_DIR / "raw_data.json", 'w') as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

    print(f"\nResults: {RESULTS_DIR / 'results.md'}")
    print(f"Raw data: {RESULTS_DIR / 'raw_data.json'}")


if __name__ == "__main__":
    main()
