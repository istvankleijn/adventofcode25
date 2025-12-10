import pathlib 


DAY = 0

test_input = """

""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    return Object()

class Object:
    def __init__(self):
        pass
    
    def run_analysis(self, *, debug=False):
        pass
    
    def get_answer1(self, *, debug=False):
        return None

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
