from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem

PIPE_TYPES = ["|", "-", "L", "J", "7", "F", "S"]
NORTH_BOUND = ["|", "L", "J", "S"]
SOUTH_BOUND = ["|", "7", "F", "S"]
EAST_BOUND = ["-", "L", "F", "S"]
WEST_BOUND = ["-", "J", "7", "S"]
CORNERS = ["J", "L", "F", "7"]
CONNECTION_MAP = {
    # NESW
    (True, False, True, False) : "|",
    (True, True, False, False) : "L",
    (True, False, False, True) : "J",
    (False, True, True, False) : "F",
    (False, False, True, True) : "7",
    (False, True, False, True) : "-",
}

start = None


def is_s_curve(p1, p2):
    match (p1, p2):
        case ("L", "J"):
            return False
        case ("L", "7"):
            return True
        case ("F", "7"):
            return False
        case ("F", "J"):
            return True


class LoopFound(Exception):
    pass


class Pipe:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.north = self.east = self.south = self.west = None

    @property
    def connections(self):
        return [x for x in [self.north, self.east, self.west, self.south] if x is not None]

    def disconnect(self, pipe):
        for dir in ["north", "east", "south", "west"]:
            if getattr(self, dir) == pipe:
                setattr(self, dir, None)


class Map:
    def __init__(self, pipes: list[list[Pipe]]):
        self.pipes = pipes
        self.h = len(pipes) - 1  # max idx, not count
        self.w = len(pipes[0]) - 1

    def connect(self, pipe):
        if pipe.type in NORTH_BOUND:
            pipe.north = self.north_of(pipe)
        if pipe.type in SOUTH_BOUND:
            pipe.south = self.south_of(pipe)
        if pipe.type in EAST_BOUND:
            pipe.east = self.east_of(pipe)
        if pipe.type in WEST_BOUND:
            pipe.west = self.west_of(pipe)

    def north_of(self, pipe):
        if pipe.y == 0:
            return None
        north_pipe = self.pipes[pipe.y - 1][pipe.x]
        if north_pipe and north_pipe.type in SOUTH_BOUND:
            return north_pipe
        return None

    def south_of(self, pipe):
        if pipe.y == self.h:
            return None
        south_pipe = self.pipes[pipe.y + 1][pipe.x]
        if south_pipe and south_pipe.type in NORTH_BOUND:
            return south_pipe
        return None

    def east_of(self, pipe):
        if pipe.x == self.w:
            return None
        east_pipe = self.pipes[pipe.y][pipe.x + 1]
        if east_pipe and east_pipe.type in WEST_BOUND:
            return east_pipe
        return None

    def west_of(self, pipe):
        if pipe.x == 0:
            return None
        west_pipe = self.pipes[pipe.y][pipe.x - 1]
        if west_pipe and west_pipe.type in EAST_BOUND:
            return west_pipe
        return None


def find_loop(pipe: Pipe, parent: Pipe, pipe_map: Map, checked: list[Pipe]):
    pipes = [(pipe, parent)]
    while pipes:
        p, prev = pipes.pop(0)
        pipe_map.connect(p)
        checked.append(p)

        possibles = [x for x in p.connections if x not in checked and x is not prev]
        if not possibles:
            checked.remove(p)
            parent.disconnect(p)
            continue

        if "S" in [p.type for p in possibles] and start != parent:
            return True

        pipes += [(p2, p) for p2 in possibles]



def solve(input):
    pipes = []
    for y, line in enumerate(input.splitlines()):
        line_pipes = []
        for x, c in enumerate(line):
            if c in PIPE_TYPES:
                line_pipes.append(Pipe(x, y, c))
                if c == "S":
                    start = line_pipes[-1]
            else:
                line_pipes.append(None)
        pipes.append(line_pipes)

    pipe_map = Map(pipes)
    pipe_map.connect(start)

    # Find loop and pull a list of it's nodes
    for x in start.connections:
        if not find_loop(x, start, pipe_map, []):
            start.disconnect(x)
            continue
        start.type = CONNECTION_MAP[tuple([x is not None for x in [start.north, start.east, start.south, start.west]])]
        node = start.connections[0]
        parent = start
        path = [start]
        while node is not start:
            path.append(node)
            parent, node = node, [x for x in node.connections if x is not parent][0]
        break

    # Remove any non-loop pipes from map so we can scan it
    for y in range(pipe_map.h + 1):
        for x in range(pipe_map.w + 1):
            if pipe_map.pipes[y][x] not in path:
                pipe_map.pipes[y][x] = None

    # Scan west-east, keeping track of inside/outside state
    inner_squares = 0
    for y in range(pipe_map.h + 1):
        outside = True
        following_pipe = False
        last_corner = None
        for x in range(pipe_map.w + 1):
            if pipe_map.pipes[y][x] is not None:  # PIPE
                if pipe_map.pipes[y][x].type in CORNERS:
                    if not following_pipe:  # ground/pipe transition
                        last_corner = pipe_map.pipes[y][x].type
                        outside = not outside
                    elif not is_s_curve(last_corner, pipe_map.pipes[y][x].type):
                        outside = not outside
                    following_pipe = not following_pipe
                elif following_pipe:
                    pass
                else:
                    outside = not outside
            else:  # NOT PIPE
                last_corner = None
                following_pipe = False
                if not outside:
                    inner_squares += 1
    return inner_squares


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    assert solve(input) == 4
    input = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""
    assert solve(input) == 4


def test_part2_example_2():
    input = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    assert solve(input) == 8


def test_part2_example_3():
    input = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    assert solve(input) == 10
