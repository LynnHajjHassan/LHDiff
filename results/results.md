# Evaluation of LHDiff

## 1. Evaluation Setup

We evaluate **LHDiff**, a line-based code differencing tool, by comparing its predicted line mappings against **normalized ground truth (GT)** mappings.

### Ground Truth

* Ground truth mappings are provided as XML files and normalized using our preprocessing pipeline.
* Each GT file defines mappings from **old file line numbers** to **new file line numbers**.
* Evaluation is performed **only on lines defined in the ground truth**, ensuring fairness.

### Metrics

We report the standard information retrieval metrics:

* **Precision**: proportion of predicted mappings that are correct
* **Recall**: proportion of ground truth mappings that were successfully found
* **F1-score**: harmonic mean of precision and recall

These metrics are computed using our custom `evaluate()` function.

---

## 2. Datasets Evaluated

We evaluated LHDiff on a diverse set of real-world code examples across multiple languages, including:

* **Java** (e.g., `GamePanel`, `Server`, `Date`)
* **Python** (e.g., `guessGame`, `random_data_library`)
* **C** (e.g., `game`, `proc`)
* **JavaScript** (e.g., `js-array`, `localStorage`)
* **PHP** (e.g., `cart`, `login`)

The datasets vary in:

* size (small scripts to large source files),
* amount of change (minor edits vs major restructuring),
* language syntax and style.

---

## 3. Quantitative Results

The table below summarizes representative evaluation results.

| Dataset             | Language   | Precision | Recall | F1   |
| ------------------- | ---------- | --------- | ------ | ---- |
| GamePanel           | Java       | 1.00      | 0.40   | 0.57 |
| Date                | Java       | 1.00      | 0.67   | 0.80 |
| Server              | Java       | 0.67      | 0.50   | 0.57 |
| Array_Data          | Java       | 1.00      | 0.40   | 0.57 |
| game                | C          | 0.86      | 0.63   | 0.73 |
| random_data_library | Python     | 1.00      | 0.77   | 0.87 |
| js-array            | JavaScript | 1.00      | 1.00   | 1.00 |
| urldecoder          | Java       | 1.00      | 1.00   | 1.00 |

---

## 4. Result Analysis

### 4.1 Precision vs Recall

Across most datasets, **precision is consistently high**, often reaching 1.0.
This indicates that when LHDiff reports a mapping, it is usually correct.

Recall varies depending on the dataset:

* **Higher recall** is observed in files with limited restructuring and consistent formatting.
* **Lower recall** appears in cases with extensive line insertions, deletions, or large structural changes.

This reflects a **conservative design choice**: LHDiff prioritizes correctness over aggressive matching.

---

### 4.2 Impact of Code Structure

LHDiff performs best on:

* structured code,
* moderate edits,
* refactorings that preserve textual similarity.

Lower performance is observed in:

* heavily reorganized files,
* generated or templated code,
* cases where semantic similarity does not align with textual similarity.

---

### 4.3 Split Detection

Split detection enables LHDiff to identify cases where a single line in the old version maps to multiple lines in the new version.
This improves accuracy in cases involving line expansions, although such mappings remain challenging under heavy restructuring.

---

## 5. Qualitative Evaluation (GUI)

For datasets without ground truth, we performed **qualitative inspection** using the LHDiff GUI.

The GUI allows:

* side-by-side visualization of old and new files,
* highlighting of mapped lines,
* manual inspection of correctness.

Visual inspection confirms that many unchanged or slightly modified lines are correctly tracked even when quantitative evaluation is unavailable.

---

## 6. Limitations

While LHDiff performs well overall, several limitations remain:

* Recall decreases under extreme restructuring.
* The approach relies primarily on textual similarity rather than semantic understanding.
* Ground truth coverage varies across datasets, affecting evaluation consistency.

These limitations suggest opportunities for future improvement.

---

## 7. Summary

Overall, LHDiff demonstrates:

* **high precision** across diverse datasets,
* **robust performance** on moderately changing code,
* effective handling of multiple programming languages,
* practical usability through GUI-based inspection.

These results validate LHDiff as a reliable and extensible line-tracking tool for code evolution analysis.

---

## 8. Future Work

Potential improvements include:

* incorporating semantic embeddings for similarity,
* improving recall for heavily restructured code,
* refining split and merge detection,
* expanding evaluation datasets.

