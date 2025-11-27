
# **LHDiff – Language-Independent Hybrid Line Mapping Tool**

## Project Structure

```
src/
 ├── preprocessing/        # Line normalization, comment/whitespace handling
 ├── similarity/           # Levenshtein, cosine similarity, SimHash
  ├── similarity_part1/                   
  ├── similarity_part2/                 
 ├── mapping/              # Candidate matching, conflict resolution
 ├── split/                # Line split/merge detection
 ├── evaluation/           # Accuracy testing, benchmarks
 └── utils/                # Helper functions

data/
 ├── old/                  # Old version files
 ├── new/                  # New version files
 └── ground_truth/         # Expected mapping for evaluation

docs/                      # Report, meeting notes, diagrams
tests/                     # Unit tests
```

---

## Branching Strategy

* **main** → Stable, reviewed, ready for submission
* **dev** → Integration of modules before merging to `main`
* **feature/...** → Individual development branches

  * `feature/preprocessing`
  * `feature/similarity`
    * `feature/similarity_part1`
    * `feature/similarity_part2`
  * `feature/mapping`
  * `feature/split-detection`
  * `feature/evaluation`
  * `feature/integration`

All code must go through a Pull Request into `dev`, then into `main`.

Here is your **final polished, clean, fair, professionally-structured task distribution**, based on difficulty, workflow order, dependencies, and each teammate’s abilities.

It reflects the actual pipeline order and keeps everything balanced.

You can copy-paste this directly into your group chat, GitHub README, or Notion page.

---

# **LHDiffTask Distribution**

# **1. Lynn — Project Lead + Similarity Part 2 + Integration**

**Responsibilities:**

* SimHash implementation
* Hamming distance + top-k candidate selection
* Full pipeline integration (connecting all modules)
* Utilities & helper functions
* Reviewing pull requests
* Ensuring module compatibility
* Final testing + cleanup

---

# **2. Luqman — Preprocessing + Mutation-Based Evaluation**

**Responsibilities:**

* `normalize_line()`
* Remove whitespace, tabs, comments
* Produce clean line arrays
* Build mutation-based test files (edit taxonomy)
* Write evaluation metrics (precision, recall, accuracy)

---

# **3. Hanan — Line Split Detection + GUI Visualization**

**Responsibilities:**

* Implement multi-line expansion loop
* Detect when similarity increases and when to stop
* Integrate split results with final mapping
* Create visualization mockups or a  Java GUI showing:

  * L lines → R lines mappings
  * Split/merged lines highlights

---

# **4. Parsia — Mapping + Conflict Resolution**

**Responsibilities:**

* Build candidate mapping structure
* Combine similarity scores (weighted 0.6 + 0.4)
* Choose best match above threshold
* Resolve collisions (two left lines matching same right line)
* Produce final mapping output

---

# **5. Noor — Similarity Part 1 + Dataset Collection**

**Responsibilities:**

* Levenshtein distance (content similarity)
* Context extraction (top/bottom 4 lines)
* Cosine similarity (context similarity)
* Collect 25+ file pairs for dataset
* Organize references + ground truth
  
---

# **Workflow Order (Modules in Sequence)**

code pipeline will follow this order:

1. **Preprocessing** (Luqman)
2. **Unchanged line detection (diff)** → (Integration)
3. **Similarity**
   * Part 1 → (Noor)
   * Part 2 → (Lynn)
4. **Candidate generation (top-k)** → (Lynn)
5. **Mapping + conflict resolution** → (Parsia)
6. **Line-split detection** → (Hanan)
7. **Evaluation (mutation + dataset)**  (Luqman + Noor)
8. **Visualization (GUI)** → (Hanan)
9. **Integration + final testing**  (Lynn)

---
