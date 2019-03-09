from math import log

# Goal:
# Input: a list of just intonation (JI) ratios
# Output: a list of EDOs that progressively approximate the given ratios better (absolutely)
#         For each such EDO, print out the tone numbers (0-indexed) that approximate the ratios in input order
# Example format: 
#   Input: [3/2, 5/4]
#   Output:
#   12 EDO (3/2: note 7 with error -2.0 cents, 5/4: note 4 with error +13.7 cents)
#   [some other EDOs, maybe]
#   58 EDO (3/2: note 34 with error +1.5 cents, 5/4: note 19 with error +6.8 cents)
#   [some more EDOs]

# EDO-record is of type {'edo': Int, 'approximations': [{'ratio': Rational, 'note_index': Int, 'error': Double}]}

# find_approximation_error: Int -> Double -> (Int, Double)
# returns (note_index, approximation_error_in_cents)
def find_approximation_error(edo_number, ratio_to_approximate):
    # hand-derived; we want to find n to approximate 2^(n/N)/R to 1 as close as possible,
    # where R = ratio_to_approximate, n = edo_number
    closest_note_index = round(edo_number * log(ratio_to_approximate) / log(2))
    expected_ratio = 2 ** (closest_note_index / edo_number)
    # from http://www.sengpielaudio.com/calculator-centsratio.htm
    approximation_error_in_cents = 1200 * (log(expected_ratio) - log(ratio_to_approximate)) / log(2)
    return (closest_note_index, approximation_error_in_cents)

# has_better_approximations: EDO-record -> EDO-record -> Boolean
# returns true if competing_edo_record has better approximations than (or equal approximation to) best_edo_so_far for every given ratio
def has_better_approximations(best_edo_so_far, competing_edo_record):
    for best_error, competing_error in zip(best_edo_so_far['approximations'], competing_edo_record['approximations']):
        if abs(best_error['error']) < abs(competing_error['error']):
            return False
    return True

# rational_to_float: String -> Double
# The strings are of the form $n/$d, so fractions.
def rational_to_float(ratio):
    numerator = float(ratio.split("/")[0])
    denominator = float(ratio.split("/")[1])
    return numerator / denominator

# find_progressively_better_edos: [String] -> [EDO-record]
# The strings are of the form $n/$d, so fractions.
def find_progressively_better_edos(ratio_input_list, lowest_edo = 12, highest_edo = 1000):
    progressively_better_edos = []
    best_edo_so_far = None
    for edo in range(lowest_edo, highest_edo + 1):
        temp_edo_record = {'edo': edo, 'approximations': []}
        for ratio in ratio_input_list:
            index, error = find_approximation_error(edo, rational_to_float(ratio))
            temp_edo_record['approximations'].append({'ratio': ratio, 'note_index': index, 'error': error})
        if best_edo_so_far is None or has_better_approximations(best_edo_so_far, temp_edo_record):
            progressively_better_edos.append(temp_edo_record)
            best_edo_so_far = temp_edo_record
    return progressively_better_edos

# print_progressively_better_edos: [EDO-record] -> Void (prints to stdout)
def print_progressively_better_edos(edo_records):
    # Example format for each record: 
    # 12 EDO (3/2: note 7 with error -2.0 cents, 5/4: note 4 with error +13.7 cents)
    for edo_record in edo_records:
        edo_approximation_strings_list = ["%s: note %d with error %s%0.2f cents" % 
            (a['ratio'], a['note_index'], '+' if a['error'] >= 0 else '-', abs(a['error']))
            for a in edo_record["approximations"]]
        edo_string = "%d EDO (%s)" % (edo_record["edo"], ", ".join(edo_approximation_strings_list))
        print(edo_string)

def main():
    ratio_input_lists = [["3/2", "5/4", "6/5", "9/8"],
        ["3/2", "5/4", "6/5", "9/8", "7/4", "9/7", "7/6", "7/5"], 
        ["3/2", "5/4", "6/5", "9/8", "7/4", "9/7", "7/6", "7/5", "11/8", "11/9"]]
    for ratio_input_list in ratio_input_lists:
        progressively_better_edos = find_progressively_better_edos(ratio_input_list, highest_edo = 200)
        print_progressively_better_edos(progressively_better_edos)
        print("")


if __name__ == "__main__":
    main()
