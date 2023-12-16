from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from sys import platform
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def solve(input):
    rows = [list(r) for r in input.splitlines()]
    width, height = len(rows[0]), len(rows)

    shifted = True
    while shifted:
        load = 0
        shifted = False
        for y in range(1, height):
            for x in range(width):
                if rows[y][x] != "O":
                    continue
                if rows[y - 1][x] == ".":
                    rows[y - 1][x] = "O"
                    rows[y][x] = "."
                    shifted = True
                else:
                    load += height - y
    load += height * rows[0].count("O")
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
    assert solve(input) == 136
