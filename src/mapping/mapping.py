# src/mapping/mapping.py

from typing import Dict, List, Tuple

THRESHOLD = 0.5  # default threshold, adjust if needed
WEIGHT_CONTENT = 0.6
WEIGHT_SIMHASH = 0.4


def combined_score(content_score: float, simhash_score: float,
                   w_content: float = WEIGHT_CONTENT,
                   w_simhash: float = WEIGHT_SIMHASH) -> float:
    """
    Combine content-based and SimHash similarity scores using given weights.
    """
    return w_content * content_score + w_simhash * simhash_score


def choose_best_match(left: int, candidates: List[int],
                      content_scores: Dict[Tuple[int,int], float],
                      simhash_scores: Dict[Tuple[int,int], float]) -> Tuple[int, float]:
    """
    Choose the best right line for a left line from top-k candidates.

    Parameters:
      left            : index of left line
      candidates      : list of right line indices from top-k (shortlist)
      content_scores  : similarity scores based on content
      simhash_scores  : similarity scores based on SimHash

    Returns:
      (best_right_line, combined_score)
    """
    best_score = -1        # start with a very low score to ensure first candidate replaces it
    best_right = None      # initially we don't know the best match

    # Loop over top-k candidates (shortlist of promising right lines)
    for right in candidates:
        content = content_scores.get((left, right), 0)
        simhash = simhash_scores.get((left, right), 0)
        score = combined_score(content, simhash)
        if score > best_score:
            best_score = score
            best_right = right

    return best_right, best_score


def resolve_conflicts(mapping: Dict[int, Tuple[int, float]]) -> Dict[int, int]:
    """
    Resolve conflicts: if two left lines map to the same right line,
    keep the left line with the higher score.

    Input mapping: {left_line: (right_line, score)}
    Output: {left_line: right_line}
    """
    right_taken = {}       # keep track of already assigned right lines
    final_mapping = {}     # final mapping to return

    # Sort left lines by decreasing score so higher-scoring matches get priority
    sorted_items = sorted(mapping.items(), key=lambda x: -x[1][1])

    for left, (right, score) in sorted_items:
        if right is None:
            continue    # skip lines with no valid match
        if right not in right_taken:
            right_taken[right] = left
            final_mapping[left] = right
        # if right is already taken → lower score is ignored (conflict resolved)

    return final_mapping


def generate_mapping(content_scores: Dict[Tuple[int,int], float],
                     simhash_scores: Dict[Tuple[int,int], float],
                     top_k: Dict[int, List[int]],
                     threshold: float = THRESHOLD) -> Dict[int, int]:
    """
    Returns a mapping: left_line_index -> right_line_index

    Parameters:
      content_scores : similarity scores based on content
      simhash_scores : similarity scores based on SimHash
      top_k          : dictionary of top-k candidates for each left line
                       e.g., top_k[0] = [0,1,2] means left line 0
                       will only consider right lines 0,1,2
      threshold      : minimum combined score to accept a match
    """
    preliminary_mapping = {}

    for left, candidates in top_k.items():
        # Pick best candidate from top-k list
        best_right, best_score = choose_best_match(left, candidates, content_scores, simhash_scores)
        if best_score is not None and best_score >= threshold:
            preliminary_mapping[left] = (best_right, best_score)
        else:
            preliminary_mapping[left] = (None, best_score)  # below threshold, ignore

    # Resolve conflicts where multiple left lines want the same right line
    final_mapping = resolve_conflicts(preliminary_mapping)
    return final_mapping


# --------------------
# MOCK TEST EXAMPLES
# --------------------
if __name__ == "__main__":
    # Example 1: simple mapping
    content_scores = { (0,0):0.9, (1,2):0.8 }
    simhash_scores = { (0,0):0.85, (1,2):0.7 }
    top_k = { 0: [0], 1: [2] }
    print("Test 1(simple mapping):", generate_mapping(content_scores, simhash_scores, top_k))  # {0:0, 1:2}

    # Example 2: conflict resolution
    content_scores = { (0,0):0.7, (1,0):0.9 }
    simhash_scores = { (0,0):0.6, (1,0):0.8 }
    top_k = { 0: [0], 1: [0] }
    print("Test 2(conflict resolution):", generate_mapping(content_scores, simhash_scores, top_k))  # {1:0}

    # Example 3: threshold test
    content_scores = { (0,0):0.3 }
    simhash_scores = { (0,0):0.4 }
    top_k = {0: [0]}
    print("Test 3(threshold test):", generate_mapping(content_scores, simhash_scores, top_k))  # {}

    # Example 4: multiple candidates
    content_scores = { (0,0):0.9, (0,1):0.88, (0,2):0.75 }
    simhash_scores = { (0,0):0.85, (0,1):0.8, (0,2):0.7 }
    top_k = {0: [0,1,2]}
    print("Test 4(multiple candidates):", generate_mapping(content_scores, simhash_scores, top_k))  # {0:0}
