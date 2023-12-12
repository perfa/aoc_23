from itertools import combinations
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def solve(input: str) -> int:
    image = input.splitlines()
    width = len(image[0])

    vertical_expansions = list(range(len(image)))
    horizontal_expansions = list(range(len(image[0])))
    original_positions = []
    for x in range(width):
        for y in range(len(image)):
            if image[y][x] == "#":
                original_positions.append((x, y))
                if y in vertical_expansions:
                    vertical_expansions.remove(y)
                if x in horizontal_expansions:
                    horizontal_expansions.remove(x)

    galaxy_pairs = list(combinations(original_positions, 2))
    total_distance = 0
    for p1, p2 in galaxy_pairs:
        x1, y1 = p1
        x2, y2 = p2
        miny, maxy = min(y1, y2), max(y1, y2)
        minx, maxx = min(x1, x2), max(x1, x2)
        vertical_change = len([e for e in vertical_expansions if miny < e < maxy])
        horizontal_change = len([e for e in horizontal_expansions if minx < e < maxx])
        total_distance += abs(x1 - x2) + abs(y1 - y2) + vertical_change + horizontal_change

    return total_distance


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    assert solve(input) == 374
