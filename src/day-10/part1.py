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

start = None


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

    for x in start.connections:
        if not find_loop(x, start, pipe_map, []):
            start.disconnect(x)
            continue
        step = start
        path = []
        while True:
            path.append(step)
            paths = [
                x for x in step.connections
                if x not in path[-2:]
            ]
            if start in paths:
                break
            step = paths[0]
        return int(len(path) / 2)


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    assert solve(input) == 4


def test_part1_example_2():
    input = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    assert solve(input) == 8
