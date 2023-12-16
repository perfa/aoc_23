from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from sys import platform
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def swirl(rows, width, height):
    shifted = True
    while shifted:
        shifted = False
        for y in range(1, height):
            for x in range(width):
                if rows[y][x] != "O":
                    continue
                if rows[y - 1][x] == ".":
                    rows[y - 1][x] = "O"
                    rows[y][x] = "."
                    shifted = True
    shifted = True
    while shifted:
        shifted = False
        for y in range(height):
            for x in range(1, width):
                if rows[y][x] != "O":
                    continue
                if rows[y][x - 1] == ".":
                    rows[y][x - 1] = "O"
                    rows[y][x] = "."
                    shifted = True
    shifted = True
    while shifted:
        shifted = False
        for y in range(height - 1):
            for x in range(width):
                if rows[y][x] != "O":
                    continue
                if rows[y + 1][x] == ".":
                    rows[y + 1][x] = "O"
                    rows[y][x] = "."
                    shifted = True
    shifted = True
    while shifted:
        shifted = False
        for y in range(height):
            for x in range(width - 1):
                if rows[y][x] != "O":
                    continue
                if rows[y][x + 1] == ".":
                    rows[y][x + 1] = "O"
                    rows[y][x] = "."
                    shifted = True


def solve(input):
    rows = [list(r) for r in input.splitlines()]
    width, height = len(rows[0]), len(rows)
    state = []

    while True:
        swirl(rows, width, height)
        platform = "\n".join(["".join(r) for r in rows])
        if state.count(platform) == 1:
            first_occurence = state.index(platform)
            loop_size = len(state) - first_occurence
            break
        state.append(platform)

    idx = (1000000000 - first_occurence) % loop_size - 1
    rows = state[first_occurence + idx].splitlines()
    load = 0
    for y, row in enumerate(rows):
        for col in row:
            if col == "O":
                load += height - y

    return load


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    assert solve(input) == 64
