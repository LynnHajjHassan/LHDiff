
#IMPORT STUFF-------------------

# Preprocessing step: this normalizes each file (remove spaces, lowercase, strip comments, etc.)
from preprocessing.preprocess import normalize_file

# Utilities (unchanged detection)
# If the unchanged_diff module isn't ready yet, we use a dummy fallback.
try:
    from utils.unchanged_diff import find_unchanged_lines
except ImportError:
    # If import fails, just return an empty list so pipeline doesn't crash.
    def find_unchanged_lines(a, b):
        return []   # fallback for now

# Similarity Part 1 (Noor's part)
# These compute Levenshtein, cosine similarity, and build context windows.
from similarity.similarity_part1.levenshtein import levenshtein
from similarity.similarity_part1.cosine import cosine_similarity
from similarity.similarity_part1.context import build_context
from similarity.similarity_part1.combined_similarity import combined_similarity

# Similarity Part 2 (Lynn's part)
# This generates the top-k most similar candidates for each line using SimHash + Hamming.
from similarity.similarity_part2.top_k import top_k_candidates

# Mapping (Parsia)
# This takes similarity scores + top-k + unchanged matches and decides final mapping.
from mapping.mapping import generate_mapping

# Split detection (Hanan)
# This checks if one line on the left actually maps to multiple lines on the right.
from split.split_detection import detect_splits



# PIPELINE FUNCTION -------------------

def run_pipeline(old_file_path: str, new_file_path: str, top_k_value: int = 15):
    """
    Complete LHDiff pipeline.
    Returns: dict[L_index -> list of R_indexes]

    (My understanding as a student:)
    - This is basically the “main function” for our whole project.
    - Each step prints what it’s doing so we can debug the workflow.
    """

    print("\n=== 1) Preprocessing files ===")
    # Normalize both files into lists of cleaned lines
    left_lines = normalize_file(old_file_path)
    right_lines = normalize_file(new_file_path)

    print(f"Left lines: {len(left_lines)}, Right lines: {len(right_lines)}")


    print("\n=== 2) Detect unchanged lines (fast matches) ===")
    # These are exact unchanged matches detected quickly (like diff)
    unchanged_pairs = find_unchanged_lines(left_lines, right_lines)
    print(f"Found {len(unchanged_pairs)} unchanged lines")


    print("\n=== 3) Similarity Part 1 (Levenshtein + Cosine) ===")
    # Computes detailed similarity scores between all pairs (content + context)
    similarity_scores = combined_similarity(left_lines, right_lines)
    print(f"Generated {len(similarity_scores)} similarity pairs")


    print("\n=== 4) Similarity Part 2 (SimHash Top-K) ===")
    # Get only the top-k most similar right lines for each left line
    # This speeds up the mapping step a lot.
    top_k = top_k_candidates(left_lines, right_lines, k=top_k_value)
    print("Top-K candidates computed")


    print("\n=== 5) Mapping (Parsia) ===")
    # Combine all similarity info to produce one final line-to-line mapping
    single_mapping = generate_mapping(similarity_scores, top_k, unchanged_pairs)
    print(f"Mapping generated for {len(single_mapping)} left lines")


    print("\n=== 6) Split Detection (Hanan) ===")
    # Detect if some lines were split into multiple lines in the new version
    final_mapping = detect_splits(left_lines, right_lines, single_mapping)

    print("\n=== PIPELINE FINISHED ===")
    return final_mapping



# TESTING ENTRY POINT -------------------

if __name__ == "__main__":
    # TEMP TEST — this is just for us to test easily by running the file directly.
    # can replace these file paths with actual old/new files in /data/.
    result = run_pipeline("data/old/GamePanel_1.java", "data/new/GamePanel_2.java")

    print("\nFinal Mapping Output:")
    print(result)
