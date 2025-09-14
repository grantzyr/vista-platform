class CriteriaService:
    """
    This class contains all the criteria for the verifier.
    """
    @staticmethod
    def blue_eq_1(context: str) -> bool:
        return int(context[0]) == 1

    @staticmethod
    def blue_gt_1(context: str) -> bool:
        return int(context[0]) > 1

    @staticmethod
    def blue_lt_3(context: str) -> bool:
        return int(context[0]) < 3

    @staticmethod
    def blue_eq_3(context: str) -> bool:
        return int(context[0]) == 3

    @staticmethod
    def blue_gt_3(context: str) -> bool:
        return int(context[0]) > 3

    @staticmethod
    def yellow_lt_3(context: str) -> bool:
        return int(context[1]) < 3

    @staticmethod
    def yellow_eq_3(context: str) -> bool:
        return int(context[1]) == 3

    @staticmethod
    def yellow_gt_3(context: str) -> bool:
        return int(context[1]) > 3

    @staticmethod
    def yellow_lt_4(context: str) -> bool:
        return int(context[1]) < 4

    @staticmethod
    def yellow_eq_4(context: str) -> bool:
        return int(context[1]) == 4

    @staticmethod
    def yellow_gt_4(context: str) -> bool:
        return int(context[1]) > 4

    @staticmethod
    def blue_is_even(context: str) -> bool:
        return int(context[0]) % 2 == 0

    @staticmethod
    def blue_is_odd(context: str) -> bool:
        return int(context[0]) % 2 == 1

    @staticmethod
    def yellow_is_even(context: str) -> bool:
        return int(context[1]) % 2 == 0

    @staticmethod
    def yellow_is_odd(context: str) -> bool:
        return int(context[1]) % 2 == 1

    @staticmethod
    def purple_is_even(context: str) -> bool:
        return int(context[2]) % 2 == 0

    @staticmethod
    def purple_is_odd(context: str) -> bool:
        return int(context[2]) % 2 == 1

    @staticmethod
    def zero_1s(context: str) -> bool:
        return context.count('1') == 0

    @staticmethod
    def one_1(context: str) -> bool:
        return context.count('1') == 1

    @staticmethod
    def two_1s(context: str) -> bool:
        return context.count('1') == 2

    @staticmethod
    def three_1s(context: str) -> bool:
        return context.count('1') == 3

    @staticmethod
    def zero_3s(context: str) -> bool:
        return context.count('3') == 0

    @staticmethod
    def one_3(context: str) -> bool:
        return context.count('3') == 1

    @staticmethod
    def two_3s(context: str) -> bool:
        return context.count('3') == 2

    @staticmethod
    def three_3s(context: str) -> bool:
        return context.count('3') == 3

    @staticmethod
    def zero_4s(context: str) -> bool:
        return context.count('4') == 0

    @staticmethod
    def one_4(context: str) -> bool:
        return context.count('4') == 1

    @staticmethod
    def two_4s(context: str) -> bool:
        return context.count('4') == 2

    @staticmethod
    def three_4s(context: str) -> bool:
        return context.count('4') == 3

    @staticmethod
    def blue_lt_yellow(context: str) -> bool:
        return int(context[0]) < int(context[1])

    @staticmethod
    def blue_eq_yellow(context: str) -> bool:
        return int(context[0]) == int(context[1])

    @staticmethod
    def blue_gt_yellow(context: str) -> bool:
        return int(context[0]) > int(context[1])

    @staticmethod
    def blue_lt_purple(context: str) -> bool:
        return int(context[0]) < int(context[2])

    @staticmethod
    def blue_eq_purple(context: str) -> bool:
        return int(context[0]) == int(context[2])

    @staticmethod
    def blue_gt_purple(context: str) -> bool:
        return int(context[0]) > int(context[2])

    @staticmethod
    def yellow_lt_purple(context: str) -> bool:
        return int(context[1]) < int(context[2])

    @staticmethod
    def yellow_eq_purple(context: str) -> bool:
        return int(context[1]) == int(context[2])

    @staticmethod
    def yellow_gt_purple(context: str) -> bool:
        return int(context[1]) > int(context[2])

    @staticmethod
    def blue_smallest(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return blue < yellow and blue < purple

    @staticmethod
    def yellow_smallest(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow < blue and yellow < purple

    @staticmethod
    def purple_smallest(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return purple < blue and purple < yellow

    @staticmethod
    def blue_largest(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return blue > yellow and blue > purple

    @staticmethod
    def yellow_largest(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow > blue and yellow > purple

    @staticmethod
    def purple_largest(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return purple > blue and purple > yellow

    @staticmethod
    def even_odd_of_num(context: str) -> tuple[int, int]:
        even_num = 0
        odd_num = 0
        for num in context:
            if int(num) % 2 == 0:
                even_num += 1
            else:
                odd_num += 1
        return even_num, odd_num

    @classmethod
    def more_even_numbers(cls, context: str) -> bool:
        even_num, odd_num = cls.even_odd_of_num(context)
        return even_num > odd_num

    @classmethod
    def more_odd_numbers(cls, context: str) -> bool:
        even_num, odd_num = cls.even_odd_of_num(context)
        return even_num < odd_num

    @classmethod
    def zero_even_numbers(cls, context: str) -> bool:
        even_num, odd_num = cls.even_odd_of_num(context)
        return even_num == 0

    @classmethod
    def one_even_number(cls, context: str) -> bool:
        even_num, odd_num = cls.even_odd_of_num(context)
        return even_num == 1

    @classmethod
    def two_even_numbers(cls, context: str) -> bool:
        even_num, odd_num = cls.even_odd_of_num(context)
        return even_num == 2

    @classmethod
    def three_even_numbers(cls, context: str) -> bool:
        even_num, odd_num = cls.even_odd_of_num(context)
        return even_num == 3

    @staticmethod
    def sum_is_even(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) % 2 == 0

    @staticmethod
    def sum_is_odd(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) % 2 == 1

    @staticmethod
    def blue_yellow_sum_lt_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow) < 6

    @staticmethod
    def blue_yellow_sum_eq_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow) == 6

    @staticmethod
    def blue_yellow_sum_gt_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow) > 6

    @staticmethod
    def triple_number(context: str) -> bool:
        return len(set(context)) == 1

    @staticmethod
    def double_number(context: str) -> bool:
        return len(set(context)) == 2

    @staticmethod
    def no_repetition(context: str) -> bool:
        return len(set(context)) == 3

    @staticmethod
    def no_pairs(context: str) -> bool:
        return len(set(context)) != 2

    @staticmethod
    def has_pair(context: str) -> bool:
        return len(set(context)) == 2

    @staticmethod
    def ascending_order(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return blue < yellow < purple

    @staticmethod
    def descending_order(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return blue > yellow > purple

    @classmethod
    def no_order(cls, context: str) -> bool:
        return not cls.ascending_order(context) and not cls.descending_order(context)

    @staticmethod
    def sum_lt_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) < 6

    @staticmethod
    def sum_eq_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) == 6

    @staticmethod
    def sum_gt_6(context: str) -> int:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) > 6

    @staticmethod
    def three_ascending(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow == blue + 1 and purple == yellow + 1

    @staticmethod
    def two_ascending(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        first_pair_ascends = yellow == blue + 1
        second_pair_ascends = purple == yellow + 1
        return first_pair_ascends != second_pair_ascends

    @staticmethod
    def no_ascending(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow != blue + 1 and purple != yellow + 1

    @staticmethod
    def purple_lt_3(context: str) -> bool:
        return int(context[2]) < 3

    @staticmethod
    def blue_lt_4(context: str) -> bool:
        return int(context[0]) < 4

    @staticmethod
    def purple_lt_4(context: str) -> bool:
        return int(context[2]) < 4

    @staticmethod
    def yellow_eq_1(context: str) -> bool:
        return int(context[1]) == 1

    @staticmethod
    def purple_eq_1(context: str) -> bool:
        return int(context[2]) == 1

    @staticmethod
    def purple_eq_3(context: str) -> bool:
        return int(context[2]) == 3

    @staticmethod
    def blue_eq_4(context: str) -> bool:
        return int(context[0]) == 4

    @staticmethod
    def purple_eq_4(context: str) -> bool:
        return int(context[2]) == 4

    @staticmethod
    def yellow_gt_1(context: str) -> bool:
        return int(context[1]) > 1

    @staticmethod
    def purple_gt_1(context: str) -> bool:
        return int(context[2]) > 1

    @staticmethod
    def purple_gt_3(context: str) -> bool:
        return int(context[2]) > 3

    @staticmethod
    def blue_smallest_or_tie(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return blue <= yellow and blue <= purple

    @staticmethod
    def yellow_smallest_or_tie(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow <= blue and yellow <= purple

    @staticmethod
    def purple_smallest_or_tie(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return purple <= blue and purple <= yellow

    @staticmethod
    def blue_largest_or_tie(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return blue >= yellow and blue >= purple

    @staticmethod
    def yellow_largest_or_tie(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow >= blue and yellow >= purple

    @staticmethod
    def purple_largest_or_tie(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return purple >= blue and purple >= yellow

    @staticmethod
    def sum_multiple_of_3(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) % 3 == 0

    @staticmethod
    def sum_multiple_of_4(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) % 4 == 0

    @staticmethod
    def sum_multiple_of_5(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow + purple) % 5 == 0

    @staticmethod
    def blue_yellow_sum_eq_4(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + yellow) == 4

    @staticmethod
    def blue_purple_sum_eq_4(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + purple) == 4

    @staticmethod
    def yellow_purple_sum_eq_4(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (yellow + purple) == 4

    @staticmethod
    def blue_purple_sum_eq_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (blue + purple) == 6

    @staticmethod
    def yellow_purple_sum_eq_6(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return (yellow + purple) == 6

    @staticmethod
    def blue_gt_4(context: str) -> bool:
        return int(context[0]) > 4

    @staticmethod
    def purple_gt_4(context: str) -> bool:
        return int(context[2]) > 4

    @staticmethod
    def yellow_lt_blue(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow < blue

    @staticmethod
    def yellow_eq_blue(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow == blue

    @staticmethod
    def yellow_gt_blue(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        return yellow > blue

    @staticmethod
    def three_in_sequence_in_ascending_or_descending(context: str) -> bool:
        blue, yellow, purple = map(int, context)
        diff1 = yellow - blue
        diff2 = purple - yellow
        return diff1 == diff2 and abs(diff1) == 1

    @classmethod
    def two_in_sequence_in_ascending_or_descending(cls, context: str) -> bool:
        if cls.three_in_sequence_in_ascending_or_descending(context):
            return False
        blue, yellow, purple = map(int, context)
        return abs(yellow - blue) == 1 or abs(purple - yellow) == 1

    @classmethod
    def no_sequence_in_ascending_or_descending(cls, context: str) -> bool:
        return not cls.two_in_sequence_in_ascending_or_descending(context) and not cls.three_in_sequence_in_ascending_or_descending(context)

