from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read().split()
output = 0
identifier = Path(__file__).stem


def solve(input):
    return "Not Implemented"


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = """TODO"""
    assert solve(input) == "Not Implemented"
