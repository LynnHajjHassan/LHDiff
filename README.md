
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
