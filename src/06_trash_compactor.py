import math
import pathlib 


DAY = 6

test_input = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    operations_line = lines[-1]
    operands_lines = lines[:-1]
    operations = list()
    operand_lengths = list()
    operand_length = -1
    for c in operations_line:
        if c in "+*":
            operations.append(c)
            operand_lengths.append(operand_length)
            operand_length = -1
        operand_length += 1
    operand_lengths.append(operand_length + 1)
    operand_lengths = operand_lengths[1:]

    if debug:
        print(f"Operations line: {operations_line!r}")
        print(f"Operations: {operations}")
        print(f"Operand lengths: {operand_lengths}")

    operands_list = list()
    char_index = 0
    problem_index = 0
    while char_index < len(operations_line) and problem_index < len(operand_lengths):
        operand_length = operand_lengths[problem_index]
        if debug:
            print(f"{operand_length=}, {char_index=}, {problem_index=}")
        operands_list.append([
            str(x[char_index:char_index+operand_length]) for x in operands_lines
        ])
        char_index += operand_length + 1
        problem_index += 1
    if debug:
        print(f"Operands: {operands_list!r}")

    problems = [
        Problem(operation, operands)
        for operation, operands in zip(operations, operands_list)
    ]
    if debug:
        print(f"Problems: {problems}")

    return Homework(problems)

class Problem:
    def __init__(self, operation: str, operands: tuple[str, ...]):
        self.operation = operation
        self.operands = operands

    def __repr__(self):
        return f"Problem({self.operation!r}, {self.operands!r})"
    
    def solve_human(self) -> int:
        if self.operation == "+":
            return sum(int(x) for x in self.operands)
        elif self.operation == "*":
            return math.prod(int(x) for x in self.operands)
        else:
            raise ValueError(f"Unknown operation: {self.operation}")
    
    def solve_cephalopod(self, *, debug=False) -> int:
        operand_length = len(self.operands[0])
        cephalopod_values = list()
        for i in range(operand_length):
            cephalopod_operand = "".join(str(x[-i]) for x in self.operands)
            cephalopod_values.append(int(cephalopod_operand))

        if self.operation == "+":
            return sum(int(x) for x in cephalopod_values)
        elif self.operation == "*":
            return math.prod(int(x) for x in cephalopod_values)
        else:
            raise ValueError(f"Unknown operation: {self.operation}")

class Homework(list):
    def solve_all_human(self):
        self.human_solutions = [problem.solve_human() for problem in self]

    def solve_all_cephalopod(self, *, debug=False):
        self.cephalopod_solutions = [
            problem.solve_cephalopod(debug=debug) for problem in self
        ]

    def run_analysis(self, *, debug=False):
        self.solve_all_human()
        self.solve_all_cephalopod()
    
    def get_answer1(self, *, debug=False):
        return sum(self.human_solutions)

    def get_answer2(self, *, debug=False):
        return sum(self.cephalopod_solutions)
    
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
