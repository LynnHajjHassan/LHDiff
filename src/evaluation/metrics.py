import statistics

def evaluate(predicted_mapping: dict[int,list[int]],
             ground_truth: dict[int,list[int]]) -> dict[str, float]:
    """
    evaluate is a method that compares a tool’s mapping(predicted mapping)
    vs the ground truth
    And assess
    """
    predicted_set = set(predicted_mapping.keys()) # we make a set of keys
    ground_set = set(ground_truth.keys())  # we make a set of keys
    mismatch_set = set() # the set of mismatches
    mismatch = 0 # the number of mismatches where its matched to the wrong line
    TP = 0 # The number of True Positives or correct matches
    FP = len(predicted_set - ground_set)  # The number of False Positives, or spurious matches
            # when tool reports a problem that doesnt exist
    FN = len(ground_set - predicted_set) # The number of False Negative or eliminate matches
                                               # missed matches
    intersect = predicted_set & ground_set # we take a list of the common matches
    for element in intersect:              # we now loop through them
        if predicted_mapping[element] == ground_truth[element]:
            TP += 1 # for every match we increase by 1
        else:
            mismatch += 1 # otherwise we increase the mismatch by 1
            mismatch_set.add(element) # we save the set of mismatches for further evaluation
    # now we evaluate those mismatches
    for miss in mismatch_set:
        diff =  abs(len(predicted_mapping[miss]) - len(ground_truth[miss])) # the difference between the
        #number of mappings to the right
        if diff < 2: # we set a limit of how much
            # we tolerate the number difference of mappings to right side
            # so a predicted mapping of L40 -> {R1, R2, R3} to the ground truth L40 -> {R1}, will fail
            # but a predicted mapping of L40 -> {R1, R2} will
            diff_median = abs(statistics.median(predicted_mapping[miss]) -
                              statistics.median(ground_truth[miss])) #
            if diff_median < 3: # if the median of the two is far off, we can assume its not a match
                TP += 1 # we increase TP if we can reasonbly assume that it is a match
            else:
                FN += 1
                FP += 1
        else:
            FN += 1 #while it may seem harsh, we increase FN and FP by 1 for each mismatch
            FP += 1 #but since we assume it be false, we can assume that the ground truth was never
                    #adressed and the program sets up a match for something that isnt a problem
    if TP + FP == 0:
        precision = 0
    else:
        precision = TP/(TP + FP)
    if TP + FN == 0:
        recall = 0
    else:
        recall = TP/(TP + FN)
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall/(precision + recall)
    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}