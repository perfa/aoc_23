from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


class Found(Exception):
    def __init__(self, amount: int) -> None:
        super().__init__()
        self.amount = amount


def reflection_value(block: list[str]) -> int:
    width, height = len(block[0]), len(block)

    for x in range(1, width):
        y = 0
        l, r = x - 1, x
        while block[y][l] == block[y][r]:
            if y == height - 1:
                y = 0
                l -= 1
                r += 1
                if l == -1 or r == width:
                    return x
            else:
                y += 1

    for y in range(1, height):
        x = 0
        u, d = y - 1, y
        while block[u][x] == block[d][x]:
            if x == width - 1:
                x = 0
                u -= 1
                d += 1
                if u == -1 or d == height:
                    return  100 * y
            else:
                x += 1
    return 0


def solve(input: str) -> int:
    block = []
    result = 0
    for line in input.splitlines():
        if line:
            block.append(line)
        else:
            result += reflection_value(block)
            block = []
    result += reflection_value(block)
    return result


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    assert solve(input) == 405


def test_part1_example_2():
    input = """########.
......###
.####.##.
.#..#.##.
....#.###
#######..
......###
##..##.##
.#..#.#..
.#..#.#..
##..##.##"""
    assert solve(input) == 900
