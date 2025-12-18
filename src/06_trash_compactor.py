import math
import pathlib 


DAY = 6

test_input = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    operations = lines[-1].strip().split()
    operands_list = list()
    for line in lines[:-1]:
        operands_list.append(
            [int(x) for x in line.strip().split()]
        )
    problems = [
        Problem(operation, operands)
        for operation, operands in zip(operations, zip(*operands_list))
    ]
    
    if debug:
        print(f"Operations: {operations}")
        print(f"Operands: {operands_list}")
        print(f"Problems: {problems}")
    return Homework(problems)

class Problem:
    def __init__(self, operation: str, operands: tuple[int, ...]):
        self.operation = operation
        self.operands = operands

    def __repr__(self):
        return f"Problem({self.operation!r}, {self.operands!r})"
    
    def solve(self) -> int:
        if self.operation == '+':
            return sum(self.operands)
        elif self.operation == '*':
            return math.prod(self.operands)
        else:
            raise ValueError(f"Unknown operation: {self.operation}")

class Homework(list):
    def solve_all(self):
        self.solutions = [problem.solve() for problem in self]
    
    def run_analysis(self, *, debug=False):
        self.solve_all()
    
    def get_answer1(self, *, debug=False):
        return sum(self.solutions)

    def get_answer2(self, *, debug=False):
        return None
    
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
