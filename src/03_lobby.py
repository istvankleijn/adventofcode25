import functools
import pathlib 


DAY = 3

test_input = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    return BatteryBankCollection([BatteryBank(line.strip()) for line in lines])


class BatteryBank:
    def __init__(self, input_string):
        self.batteries = [int(c) for c in input_string]
    
    def __str__(self):
        return "".join(str(b) for b in self.batteries)
    
    def __len__(self):
        return len(self.batteries)
    
    @functools.cached_property
    def joltage(self):
        jolt = 0
        for i in range(len(self) - 1):
            for j in range(i + 1, len(self)):
                test_jolt = 10 * self.batteries[i] + self.batteries[j]
                if test_jolt > jolt:
                    jolt = test_jolt
        return jolt
    
    @functools.cache
    def overdrive_joltage(self, n_batteries=12, debug=False):
        battery_positions = list(range(len(self) - n_batteries, len(self)))
        for battery_index in range(n_batteries):
            test_position = battery_positions[battery_index]
            battery_position = battery_positions[battery_index]
            leftmost_position = battery_positions[battery_index - 1] + 1 if battery_index > 0 else 0
            if debug:
                print(f"Choosing battery {battery_index} starting at position {battery_position}")
                print(f"  Testing positions from {test_position} down to {leftmost_position}")
            while test_position >= leftmost_position:
                test_jolt = self.batteries[test_position]
                battery_jolt = self.batteries[battery_position]
                if debug:
                    print(f"  Testing position {test_position} with jolt {test_jolt} against current battery position {battery_position} with jolt {battery_jolt}")
                if test_jolt >= battery_jolt:
                    if debug:
                        print(f"    Found better battery at position {test_position} with jolt {test_jolt}")
                    battery_position = test_position
                test_position -= 1
            battery_positions[battery_index] = battery_position
        str_jolt = "".join(str(self.batteries[pos]) for pos in battery_positions)
        if debug:
            print(f"Overdrive joltage for {self} with {n_batteries} batteries: {str_jolt}")
        return int(str_jolt)
            

class BatteryBankCollection(list):
    def __init__(self, banks):
        super().__init__(banks)
        self.joltages = []
        self.overdrive_joltages = []
    
    def __str__(self):
        return "\n".join(str(bank) for bank in self)
    
    def calculate_joltages(self, debug=False):
        self.joltages = []
        for bank in self:
            self.joltages.append(bank.joltage)
    
    def calculate_overdrive_joltages(self, n_batteries=12, debug=False):
        self.overdrive_joltages = []
        for bank in self:
            self.overdrive_joltages.append(bank.overdrive_joltage(n_batteries, debug=debug))
    
    def run_analysis(self, *, debug=False):
        self.calculate_joltages(debug=debug)
        self.calculate_overdrive_joltages(debug=debug)
    
    def get_answer1(self, *, debug=False):
        return sum(self.joltages)

    def get_answer2(self, *, debug=False):
        return sum(self.overdrive_joltages)
    
    def get_answers(self, *, debug=False):
        answer1 = self.get_answer1(debug=debug)
        answer2 = self.get_answer2(debug=debug)
        return answer1, answer2


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
