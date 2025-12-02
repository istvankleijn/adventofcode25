import collections
import pathlib
import re


DAY = 1


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)


def parse(lines, *, debug=False):
    valid_move = re.compile("^(L|R)[0-9]+$")
    moves = collections.deque()
    for (i, line) in enumerate(lines):
        move = line.strip()
        assert re.fullmatch(valid_move, move), f"Invalid move {i}: {move}"
        moves.append(Move(move))
    return Dial(moves)


class Move:
    def __init__(self, input: str):
        direction, rotation = input[0], input[1:]
        if rotation == "":
            rotation = "0"
        self.direction = direction
        self.rotation = int(rotation)
    
    def __str__(self) -> str:
        return f"{self.direction}{self.rotation}"

class Dial:
    def __init__(self, pending_moves = collections.deque(), starting_rotation = 50, clicks = 100):
        self.current_rotation = starting_rotation
        self.pending_moves = pending_moves
        self.past_moves = list()
        self.rotations_visited = [starting_rotation]
    
    def run_analysis(self, *, debug=False):
        while self.pending_moves:
            move = self.pending_moves.popleft()
            if debug:
                print(f"From {self.current_rotation}, move {move}")
            if move.direction == "L":
                rotation = -move.rotation
            else:
                rotation = move.rotation
            self.current_rotation = (self.current_rotation + rotation) % 100
            if debug:
                print(f"to {self.current_rotation}")
            self.past_moves.append(move)
            self.rotations_visited.append(self.current_rotation)
        if debug:
            print(f"Visited rotations: {self.rotations_visited}")
    
    def get_answer1(self, *, debug=False):
        return self.rotations_visited.count(0)

    def get_answer2(self, *, debug=False):
        return None
    
    def get_answers(self, *, debug=False):
        answer1 = self.get_answer1(debug=debug)
        answer2 = self.get_answer2(debug=debug)
        return answer1, answer2

test_input = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
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
