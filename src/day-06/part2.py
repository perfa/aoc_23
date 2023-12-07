from functools import reduce
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def solve(input):
    time, distance = [
        int(line.split(":")[1].replace(" ", ""))
        for line in input.splitlines()
    ]

    count = 0
    lo_found = False
    for duration in range(1, time):
        if (duration * (time - duration)) > distance:
            lo_found = True
            count += 1
        elif lo_found:
            break
    return count


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = """Time:      7  15   30
Distance:  9  40  200"""
    assert solve(input) == 71503
