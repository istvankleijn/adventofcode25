import pathlib 


DAY = 7

test_input = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    return TachyonManifold(lines)

class TachyonManifold:
    def __init__(self, diagram_off: list[str]):
        self.diagram_off = diagram_off

    def create_diagram_on(self, *, debug=False):
        if debug:
            print(
                "Initial diagram when off:\n" +
                "\n".join(self.diagram_off)
            )
        self.diagram_on = list()
        self.split_count = 0
        next_row_illuminated = ["_"] * len(self.diagram_off[0])
        for this_row_when_off in self.diagram_off:
            this_row_when_on = list(this_row_when_off)
            this_row_illuminated = next_row_illuminated.copy()
            if debug:
                print(
                    "-----\n",
                    "Processing row when off:       ", "".join(this_row_when_off),
                    "\n Illuminated from previous row: ", "".join(this_row_illuminated),
                )
            for i, char in enumerate(this_row_when_off):
                match char:
                    case "S" | "|":
                        pass
                    case "^":
                        if this_row_illuminated[i] == "*":
                            self.split_count += 1
                            this_row_when_on[i - 1] = "|"
                            this_row_when_on[i + 1] = "|"
                    case ".":
                        if this_row_illuminated[i] == "*":
                            this_row_when_on[i] = "|"         
            self.diagram_on.append("".join(this_row_when_on))
            next_row_illuminated = ["*" if c in "S|" else "_" for c in this_row_when_on]
            if debug:
                print(
                    " Resulting row when on:         ", "".join(this_row_when_on),
                    "\n Illuminated for next row:      ", "".join(next_row_illuminated),
                    "\n-----\n"
                )
        if debug:
            print(
                "Final diagram when on:\n" +
                "\n".join(self.diagram_on)
            )
        return self.diagram_on

    def run_analysis(self, *, debug=False):
        self.create_diagram_on(debug=debug)
    
    def get_answer1(self, *, debug=False):
        return self.split_count

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
