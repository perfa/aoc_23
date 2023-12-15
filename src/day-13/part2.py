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
        num_wrong = 0
        y = 0
        l, r = x - 1, x
        while block[y][l] == block[y][r] or num_wrong < 2:
            if block[y][l] != block[y][r]:
                num_wrong += 1
            if y == height - 1:
                y = 0
                l -= 1
                r += 1
                if l == -1 or r == width:
                    if num_wrong == 1:
                        return x
                    break
            else:
                y += 1

    for y in range(1, height):
        num_wrong = 0
        x = 0
        u, d = y - 1, y
        while block[u][x] == block[d][x] or num_wrong < 2:
            if block[u][x] != block[d][x]:
                num_wrong += 1
            if x == width - 1:
                x = 0
                u -= 1
                d += 1
                if u == -1 or d == height:
                    if num_wrong == 1:
                        return 100 * y
                    break
            else:
                x += 1

    assert False, "Should have found a solution."


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


def test_part2_example_1():
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
    assert solve(input) == 400
