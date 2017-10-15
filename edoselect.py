from math import log

def find_ratio_squared_error(edo, actual_ratio):
    cur_error = (1200 * log(1 / actual_ratio) / log(2)) ** 2
    for i in range(1, edo + 1):
        cur_error = min(cur_error, (1200 * log(2 ** (i/edo) / actual_ratio) / log(2)) ** 2)
    return cur_error

def find_ratio_error(edo, actual_ratio):
    cur_error = 1200 * log(1 / actual_ratio) / log(2)
    for i in range(1, edo + 1):
        potential_error = 1200 * log(2 ** (i/edo) / actual_ratio) / log(2)
        if abs(potential_error) < abs(cur_error):
            cur_error = potential_error

    return cur_error


def find_edo_error5(edo):
    return 4 * find_ratio_squared_error(edo, 6/5) + 9 * find_ratio_squared_error(edo, 5/4) + 16 * find_ratio_squared_error(edo, 3/2)

def find_edo_long_error5(edo):
    return {"perfect_fifth_error": find_ratio_error(edo, 3/2), "major_third_error": find_ratio_error(edo, 5/4), "minor_third_error": find_ratio_error(edo, 6/5)}

def print_edo_long_error5(edo_long_error):
    print("3/2: " + str(round(edo_long_error["perfect_fifth_error"], 2)) + ", 5/4: " + str(round(edo_long_error["major_third_error"], 2)) + 
            ", 6/5: " + str(round(edo_long_error["minor_third_error"], 2)))


def find_edo_error7(edo):
    return find_ratio_squared_error(edo, 7/4) + 4 * find_ratio_squared_error(edo, 6/5) + 9 * find_ratio_squared_error(edo, 5/4) + 16 * find_ratio_squared_error(edo, 3/2)

def find_edo_long_error7(edo):
    return {"perfect_fifth_error": find_ratio_error(edo, 3/2), "major_third_error": find_ratio_error(edo, 5/4), "minor_third_error": find_ratio_error(edo, 6/5), "natural_seventh_error": find_ratio_error(edo, 7/4)}

def print_edo_long_error7(edo_long_error):
    print("3/2: " + str(round(edo_long_error["perfect_fifth_error"], 2)) + ", 5/4: " + str(round(edo_long_error["major_third_error"], 2)) + 
            ", 6/5: " + str(round(edo_long_error["minor_third_error"], 2)) + ", 7/4: " + str(round(edo_long_error["natural_seventh_error"], 2)))


def find_beaten_list(min_edo, max_edo, error_func, long_error_func):
    edo_errors = []
    for edo in range(min_edo, max_edo + 1):
        edo_errors.append({"edo": edo, "error": error_func(edo), "long_error": long_error_func(edo)})
        
    minimal_pair = edo_errors[0]
    beaten_list = [minimal_pair]

    for pair in edo_errors:
        if (pair["error"] < minimal_pair["error"]):
            minimal_pair = pair
            beaten_list.append(pair)

    return beaten_list


def print_beaten_list(beaten_list, print_long_error_func):
    if len(beaten_list) == 0:
        return

    print(str(beaten_list[0]["edo"]) + "-EDO with error " + str(round(beaten_list[0]["error"], 2)))
    print_long_error_func(beaten_list[0]["long_error"])

    minimal_pair = beaten_list[0]
    for pair in beaten_list[1:]:
        if pair["error"] < minimal_pair["error"]:
            print("Beaten by " + str(pair["edo"]) + "-EDO with error " + str(round(pair["error"], 2)))
            print_long_error_func(pair["long_error"])
            minimal_pair = pair


def main():
    print("Good perfect fifths, major thirds, minor thirds")
    beaten_list5 = find_beaten_list(12, 1000, find_edo_error5, find_edo_long_error5)
    print_beaten_list(beaten_list5, print_edo_long_error5)

    print()
    print("Good perfect fifths, major thirds, minor thirds, natural sevenths")
    beaten_list7 = find_beaten_list(12, 1000, find_edo_error7, find_edo_long_error7)
    print_beaten_list(beaten_list7, print_edo_long_error7)


if __name__ == "__main__":
    main()
