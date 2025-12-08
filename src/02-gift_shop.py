import collections
import pathlib 


DAY = 2


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    all_input = "".join(lines).strip()
    ranges = RangesList(
        [Range.fromstring(range) for range in all_input.split(",")]
    )
    if debug:
        print(f"Parsed ranges: {ranges}")
    return ranges

class Range:
    def __init__(self, begin: str, end: str):
        self.begin = begin
        self.end = end
    
    def __str__(self) -> str:
        return f"{self.begin}-{self.end}"

    @classmethod
    def fromstring(cls, input_string: str):
        try:
            begin, end = input_string.split("-")
        except ValueError:
            print(f"Warning: invalid range format: '{input_string}'")
            begin, end = "0", "0"
        return cls(str(begin), str(end))


class RangesListLike(list):
    def __init__(self, iterable=()):
        super().__init__(iterable)
    
    def __str__(self) -> str:
        return ", ".join(str(r) for r in self)

class RangesList(RangesListLike):
    def __init__(self, iterable=()):
        super().__init__(iterable)
        self.atomic_ranges = RangesListLike()
        self.invalid_ids = set()
    
    def find_atomic_ranges(self, *, debug=False):
        # 1. split ranges spanning odd/even lengths
        # 2. invalid IDs come from all-even length ranges only
        # 3. for all-even length ranges, split into ranges based on first half of string
        # 4. find matching first/second halves to determine invalid IDs
        # 5. save somewhere
        tmp = collections.deque(self)
        while tmp:
            range = tmp.popleft()
            if debug:
                print(f"Analyzing range: {range}")

            if len(range.begin) < len(range.end):
                range1 = Range(range.begin, "9" * len(range.begin))
                range2 = Range("1" + "0" * len(range.begin), range.end)
                if debug:
                    print(f"Split into two: {range1} and {range2}")
                tmp.append(range1)
                tmp.append(range2)
            elif len(range.begin) % 2 == 1:
                if debug:
                    print(f"No invalid IDs in range {range}")
                continue
            else:
                half_length = len(range.begin) // 2
                first_half_begin = int(range.begin[:half_length])
                first_half_end = int(range.end[:half_length])
                if first_half_end > first_half_begin:
                    range1 = Range(
                        range.begin, 
                        str(first_half_begin) + "9" * half_length
                    )
                    range2 = Range(
                        str(first_half_begin + 1) + "0" * half_length,
                        range.end
                    )
                    if debug:
                        print(f"Split into parts: {range1} and {range2}")
                    tmp.append(range1)
                    tmp.append(range2)
                else:
                    if debug:
                        print(f"Atomic range found: {range}")
                    self.atomic_ranges.append(range)
    
    def run_analysis(self, *, debug=False):
        self.find_atomic_ranges(debug=debug)
        if debug:
            print(f"Atomic even ranges: {self.atomic_ranges}")
        for range in self.atomic_ranges:
            half_length = len(range.begin) // 2
            first_half = int(range.begin[:half_length])
            second_half_begin = int(range.begin[half_length:])
            second_half_end = int(range.end[half_length:])
            if second_half_begin <= first_half <= second_half_end:
                invalid_id = 2 * str(first_half)
                if debug:
                    print(f"Found invalid ID: {invalid_id}")
                self.invalid_ids.add(invalid_id)
    
    def get_answer1(self, *, debug=False):
        return sum([int(id) for id in self.invalid_ids])

    def get_answer2(self, *, debug=False):
        return None
    
    def get_answers(self, *, debug=False):
        answer1 = self.get_answer1(debug=debug)
        answer2 = self.get_answer2(debug=debug)
        return answer1, answer2

test_input = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
""".strip()
def test():
    lines = test_input.splitlines()
    object = parse(lines, debug=True)
    object.run_analysis(debug=True)
    test1, test2 = object.get_answers(debug=True)
    print(f"Test 1: {test1}\nTest 2: {test2}")

if __name__ == "__main__":
    test()
    lines = read_file(DAY)
    object = parse(lines)
    object.run_analysis()
    answer1, answer2 = object.get_answers()
    print(f"Answer 1: {answer1}\nAnswer 2: {answer2}")
