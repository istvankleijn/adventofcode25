import itertools
import math
import pathlib 


DAY = 8

test_input = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()


def read_file(day: int):
    file = pathlib.Path("data") / f"{day:02}.txt"
    with open(file, "r") as handle:
        lines = handle.readlines()
    return(lines)

def parse(lines, *, debug=False):
    boxes = list()
    for line in lines:
        x, y, z = (int(part) for part in line.strip().split(","))
        boxes.append(JunctionBox(x, y, z))
    return Rigging3D(boxes)

class JunctionBox:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.connections = set()
    
    def __repr__(self):
        return f"JunctionBox({self.x}, {self.y}, {self.z})"
    
    def connect(self, other):
        self.connections.add(other)

class Rigging3D:
    def __init__(self, objects):
        self.objects = list(objects)
        self.circuits = {i: {i} for i in range(len(self.objects))}
    
    def __repr__(self):
        return f"Rigging3D({self.objects!r})"
    
    def __index__(self, index):
        return self.objects[index]
    
    def calculate_distances(self, debug=False):
        self.distances = dict()
        n_objects = len(self.objects)
        for j in range(n_objects):
            for i in range(j):
                obj1 = self.objects[i]
                obj2 = self.objects[j]
                dist = math.sqrt(
                    (obj1.x - obj2.x) ** 2 +
                    (obj1.y - obj2.y) ** 2 +
                    (obj1.z - obj2.z) ** 2
                )
                self.distances[(i, j)] = dist
                if debug:
                    print(f"Distance between object {i} and {j}: {dist:.3f}")
        return self.distances
    
    def connect_objects(self, n_connections, *, debug=False):
        sorted_distances = sorted(
            self.distances.items(),
            key=lambda item: item[1]
        )
        self.connections = list()
        for (i, j), dist in sorted_distances[:n_connections]:
            self.connections.append((i, j))
            self.objects[i].connect(j)
            self.objects[j].connect(i)
            new_circuit = self.circuits[i].union(self.circuits[j])
            for k in new_circuit:
                self.circuits[k] = new_circuit
            if debug:
                print(f"Connecting object {i} and {j} with distance {dist:.3f}")
                print(f"  Circuit created: {new_circuit}")
        if debug:
            print(f"Circuits: {self.circuits}")
    
    def find_circuits(self, *, debug=False):
        for i, obj in enumerate(self.objects):
            for _, circuit in self.circuits.items():
                if i in circuit:
                    if debug:
                        print(f"Add object {i} and connections {obj.connections} to existing circuit {circuit}")
                    circuit.add(i)
                    circuit.update(obj.connections)

    def run_analysis(self, *, n_connections=1000, debug=False):
        if debug:
            print(f"Running analysis on {self!r}...")
        self.calculate_distances(debug=debug)
        self.connect_objects(n_connections, debug=debug)
        self.find_circuits(debug=debug)
    
    def get_answer1(self, *, n_largest=3, debug=False):
        unique_circuits = set(frozenset(circuit) for circuit in self.circuits.values())
        unique_circuits = sorted(
            unique_circuits,
            key=lambda circuit: len(circuit),
            reverse=True
        )
        if debug:
            print(f"Unique circuits: {unique_circuits}")
        return math.prod(len(circuit) for circuit in unique_circuits[:n_largest])

    def get_answer2(self, *, debug=False):
        return None
    
    def get_answers(self, *, debug=False):
        answer1 = self.get_answer1(debug=debug)
        answer2 = self.get_answer2(debug=debug)
        return answer1, answer2


def test():
    lines = test_input.splitlines()
    object = parse(lines, debug=True)
    object.run_analysis(n_connections=3, debug=True)
    test1, test2 = object.get_answers(debug=True)
    print(f"Test 1: {test1}\nTest 2: {test2}")

if __name__ == "__main__":
    test()
    lines = read_file(DAY)
    object = parse(lines)
    object.run_analysis()
    answer1, answer2 = object.get_answers()
    print(f"Answer 1: {answer1}\nAnswer 2: {answer2}")
