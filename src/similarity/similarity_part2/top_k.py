from .simhash import simhash
from .hamming import hamming_distance


"""
For each line in left_lines, return the indexes of the top-k most similar
right-side lines (using SimHash + Hamming distance).
"""
def top_k_candidates(left_lines, right_lines, k=15):

    # Compute SimHash for every line on both sides (preprocessing step)
    left_hashes = [simhash(line) for line in left_lines]
    right_hashes = [simhash(line) for line in right_lines]

    result = {}

    # For every line on the left file
    for i, lh in enumerate(left_hashes):

        similarities = []

        # Compare with every line on the right file
        for j, rh in enumerate(right_hashes):

            # Smaller distance means more similar
            dist = hamming_distance(lh, rh)

            # Convert distance to a similarity score between 0 and 1
            score = 1 - (dist / 64)

            # Save score + index of the right side line
            similarities.append((score, j))

        # Sort by score (highest to lowest)
        similarities.sort(reverse=True)

        # Choose only the top-k right-line indexes
        top_indexes = [idx for (_, idx) in similarities[:k]]

        # Save to result dictionary
        result[i] = top_indexes

    return result       
