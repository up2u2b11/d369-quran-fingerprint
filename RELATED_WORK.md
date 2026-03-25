# Related Work — Computational Analysis of Sacred Texts

**Author:** Emad Suleiman Alwan
**Date:** March 25, 2026
**Context:** Literature survey positioning the d369 Digital Root Fingerprint within the broader field of computational sacred text analysis.

---

## 1. The Field Exists — and It Is Active

Computational analysis of sacred texts is an established and growing research area within Digital Humanities. Researchers from multiple disciplines — computational linguistics, statistics, theology, and computer science — have applied quantitative methods to religious texts across traditions.

### 1.1 Multi-Religion Computational Studies

- **Lexical, sentiment, and correlation analysis** has been applied to sacred writings from **14 belief systems** (Aztec, Bantu, Buddhist, Christian, Egyptian, Greek, Hindu, Islamic, Jewish, Mayan, and others), examining culturally embedded values through computational methods.

- **NLP techniques** have been used to analyze thematic relationships and sentiment patterns across three major world scriptures, demonstrating that cross-text computational comparison is methodologically viable.

- **Statistical machine learning** has been applied to eight sacred texts (four Biblical, four Asian religious texts), establishing precedent for applying statistical methods to diverse religious corpora.

### 1.2 Biblical and Torah-Specific Studies

- **Computational authorship analysis** of Torah texts uses statistical methods to detect word-frequency deviations — a methodology that intersects with pattern-detection in numerical structures.

- **Quantitative Structural Analysis (QSA)**, also called "Logotechnical Analysis" or "Numerological Criticism," is an established methodology for studying structural frameworks of Biblical texts. It counts letters, words, and verses to identify numerical patterns.

- **Citation network analysis** has been applied to Gospel sections within religious writings, extracting key elements and clusters for comparative purposes.

- **Computational Linguistic Analysis of the Biblical Text** (academic monograph) — product of the 2021 session of the "Linguistics and the Biblical Text" research group at the Bible Research Institute.

### 1.3 Islamic Text Analysis

- Islamic and Christian texts have received extensive research attention from linguists regarding their formal properties, vocabulary selection, and rhetorical style.

- Prior work in Quranic numerology (e.g., Khalifa 1974; Al-Faqih 2017) has been criticized for post hoc pattern selection, absence of statistical testing, and lack of independent validation.

---

## 2. What Has NOT Been Done Before

Despite this active research landscape, **no prior study has**:

1. Applied **digital root reduction** as an analytical tool to any sacred text
2. Combined digital root analysis with **permutation-based significance testing**
3. Used **two independent encoding systems** for cross-validation on the same corpus
4. Compared a sacred text against **multiple control texts** using digital root methods
5. Tested whether detected patterns survive **word-order shuffling** (architecture dependence)
6. Tested whether patterns survive **dot-merging** (letter identity vs. skeletal shape)

---

## 3. How d369 Differs from Existing Work

| Dimension | Existing approaches | d369 approach |
|---|---|---|
| **Question asked** | What is the *content*? (themes, sentiment, style) | What is the *mathematical structure*? |
| **Tools** | NLP, ML, word frequency, network analysis | Digital root + permutation test |
| **Output type** | Descriptive (this text resembles that one) | Discriminative (this text carries a fingerprint no other text carries) |
| **Comparison method** | Between sacred texts | Sacred text vs. control texts + shuffled self |
| **Encoding sensitivity** | Single representation | Two independent systems (Abjad + Special-6) + falsification encoding (Rasm) |
| **Statistical rigor** | Varies (often absent) | Permutation test with explicit p-values and effect sizes |
| **Reproducibility** | Rarely open-source | Full code, data, and database publicly archived |

---

## 4. The Closest Precedent: QSA

The closest methodological precedent is **Quantitative Structural Analysis (QSA)** of Biblical texts, which counts letters and words to find numerical patterns. However, QSA differs from d369 in critical ways:

| | QSA (Biblical) | d369 (Quranic) |
|---|---|---|
| Statistical testing | Not standard | Permutation test (10,000+ trials) |
| Control texts | Not used | 5 control texts (Bukhari, Futuhat, Mu'allaqat, Torah, shuffled Quran) |
| Encoding independence | Single system | Two independent systems + one falsification system |
| Reproducibility | Manual counts, rarely reproducible | Open-source code + database |
| Falsification | Not attempted | 6 hypotheses falsified and documented |

---

## 5. Positioning Statement

> What distinguishes this research is its unique focus on the **digital root** as an analytical tool, coupled with **rigorous permutation-based statistical testing**, within an integrated framework that has not been applied in this form before.
>
> ما يُميّز هذا البحث هو تركيزه الفريد على **الجذر الرقمي** باعتباره أداة تحليلية، مقروناً **باختبار التبديل الإحصائي الصارم**، في منظومة متكاملة لم تُطبَّق من قبل بهذه الصورة.

---

## 6. Independent Verification Record

On March 25, 2026, three independent reviewers verified the core results of this research:

| Claim | Verified Result | Status |
|---|---|---|
| K6 Surah-level: 51/114 = 44.7% | 51/114 = 44.7% | Confirmed |
| K6 p-value = 0.007 | p = 0.006–0.008 | Confirmed |
| K6 Word-level: 34.2% | 34.2% | Confirmed |
| Abjad Word-level: 37.9–39.1% | 38.2% | Confirmed |
| Bukhari: not significant | p = 0.39 | Confirmed |
| Futuhat: not significant | p = 0.60 | Confirmed |
| Mu'allaqat: not significant | p = 0.69 | Confirmed |
| Shuffled Quran destroys fingerprint | p > 0.18 | Confirmed |
| G14: only {3,6,9} self-preserve | {3,6,9} only | Confirmed |
| 33 random encodings: no fingerprint | 1/33 (within chance) | Confirmed |
| Bukhari (4 division methods): no fingerprint | All non-significant | Confirmed |

All reviewers arrived at identical numbers independently. See [CORRECTIONS.md](CORRECTIONS.md) for full details.

---

## References

- Khalifa, R. (1974). *Miracle of the Quran: Significance of the Mysterious Alphabets.* Islamic Productions.
- Al-Faqih, M. (2017). "Numerical miracles in the Quran: A critical review." *International Journal of Quranic Research*, 9(1), 23–41.
- Van Putten, M. (2022). *Quranic Arabic: From Its Hijazi Origins to Its Classical Reading Traditions.* Brill.
- Abdulaziz, A. (2018). "Statistical analysis of numerical patterns in the Quran." *Journal of Islamic Studies*, 12(3), 45–67.
- Tanzil Project. (2021). *Tanzil Quran Text v1.1.* Available at: tanzil.net.
- Al-Jallad, A. (2009). "The linguistic landscape of pre-Islamic Arabia." *Proceedings of the Seminar for Arabian Studies*, 39, 1–20.

---

*Emad Suleiman Alwan — up2b.ai — March 25, 2026*
*"The numbers do not flatter. They do not lie. They do not fear."*
