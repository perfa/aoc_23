from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def solve(input):
    result = 0
    for line in input.split():
        line = [x for x in line if x.isdigit()]
        result += int(line[0]) * 10 + int(line[-1])

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
    input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    assert solve(input) == 142
