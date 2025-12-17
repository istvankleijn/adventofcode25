import pathlib 


DAY = 5

test_input = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    fresh_ranges = list()
    ingredients = list()
    for line in lines:
        if debug:
            print(f"Parsing {line=}")
        line = line.strip()
        try:
            start, stop = line.split("-")
            if debug:
                print(f"  Found fresh range: {start=} {stop=}")
            fresh_ranges.append(range(int(start), int(stop) + 1))
        except ValueError:
            if line == "":
                continue
            ingredient = int(line)
            if debug:
                print(f"  Found ingredient: {ingredient=}")
            ingredients.append(ingredient)
    
    inventory = Inventory(fresh_ranges, ingredients)
    if debug:
        print("Parsed inventory:\n", inventory)
    return inventory

class Inventory:
    def __init__(self, fresh_ranges, ingredients):
        self.fresh_ranges = fresh_ranges
        self.ingredients = ingredients
    
    def __str__(self):
        s = ""
        for r in self.fresh_ranges:
            s += f"{r.start}-{r.stop - 1}\n"
        s += "\n"
        for ingredient in self.ingredients:
            s += f"{ingredient}\n"
        return s

    def determine_freshness(self, *, debug=False):
        self.fresh_ingredients = list()
        for ingredient in self.ingredients:
            if any(ingredient in r for r in self.fresh_ranges):
                if debug:
                    print(f"Ingredient {ingredient} is fresh.")
                self.fresh_ingredients.append(ingredient)
            else:
                if debug:
                    print(f"Ingredient {ingredient} is spoiled.")

    def run_analysis(self, *, debug=False):
        self.determine_freshness(debug=debug)
    
    def get_answer1(self, *, debug=False):
        return len(self.fresh_ingredients)

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
