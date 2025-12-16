import pathlib 


DAY = 4

test_input = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    fp = FloorPlan(lines)
    if debug:
        print("Parsed Floor Plan:")
        print(fp)
    return fp

class FloorPlan:
    def __init__(self, lines):
        self.m = len(lines) + 2
        self.n = len(lines[0].strip()) + 2
        empty_row = ["." ] * self.n
        self.grid = list([empty_row])
        for line in lines:
            row = ["."] + [c for c in line.strip()] + ["."]
            assert(len(row) == self.n)
            self.grid.append(row)
        self.grid.append(empty_row)
        self.rolls_removed = list()
    
    def __str__(self):
        s = ""
        for row in self.grid:
            s += "".join(row) + "\n"
        return s
    
    def count_adjacent_rolls(self, i, j):
        deltas = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1),  (1, 0), ( 1, 1)]
        count = 0
        for di, dj in deltas:
            neighbour_i, neighbour_j = i + di, j + dj
            if self.grid[neighbour_i][neighbour_j] == "@":
                count += 1
        return count

    def create_accessibility_plan(self, debug=False):
        self.accessibility_grid = [
            ["." for _ in range(self.n)]
            for _ in range(self.m)
        ]
        for i in range(1, self.m - 1):
            for j in range(1, self.n - 1):
                c = self.grid[i][j]
                if c == ".":
                    continue
                adjacent_rolls = self.count_adjacent_rolls(i, j)
                if adjacent_rolls < 4:
                    self.accessibility_grid[i][j] = "x"
                else:
                    self.accessibility_grid[i][j] = "@"

        self.accessibility_plan = ""
        for row in self.accessibility_grid:
            self.accessibility_plan += "".join(row) + "\n"
        if debug:
            print("Accessibility Plan:")
            print(self.accessibility_plan)
        return self.accessibility_plan
    
    def remove_accessible_rolls(self, *, debug=False):
        for i, row in enumerate(self.accessibility_plan.splitlines()):
            for j, c in enumerate(row.strip()):
                if c == "x":
                    self.grid[i][j] = "."
        if debug:
            print("Updated Floor Plan after removing accessible rolls:")
            print(self)
    
    def run_analysis(self, *, debug=False):
        self.first_plan = self.create_accessibility_plan(debug=debug)
        self.rolls_removed.append(self.n_accessible_rolls(debug=debug))
        while self.n_accessible_rolls(debug=debug):
            self.remove_accessible_rolls(debug=debug)
            self.create_accessibility_plan(debug=debug)
            self.rolls_removed.append(self.n_accessible_rolls(debug=debug))
    
    def n_accessible_rolls(self, *, debug=False):
        n_accessible_rolls = 0
        for row in self.accessibility_grid:
            for c in row:
                if c == "x":
                    n_accessible_rolls += 1
        return n_accessible_rolls
    
    def get_answer1(self, *, debug=False):
        return self.rolls_removed[0]

    def get_answer2(self, *, debug=False):
        return sum(self.rolls_removed)
    
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
