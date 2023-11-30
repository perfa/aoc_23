import sys
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
final_input = len(sys.argv) == 1
input = open(Path(__file__).parent / ("input.txt" if final_input else "example_input.txt")).read().split()
output = open(Path(__file__).parent / ("output.txt" if final_input else "example_output.txt")).read().split()
identifier = Path(__file__).stem


def solve(input):
    return "Not Implemented"


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    if result == output:
        prefix = "✅ " + Back.GREEN + Fore.WHITE
    else:
        prefix = "❌ " + Back.RED + Fore.WHITE

    print(f"\t{prefix}{result}{Style.RESET_ALL}\t{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    assert True == None
