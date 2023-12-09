from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def solve(input):
    result = 0
    for line in input.splitlines():
        values = [int(x) for x in line.split()]
        final_values = [values[-1]]

        diffs = values
        while any(diffs):
            diffs = [diffs[x + 1] - diffs[x] for x in range(len(diffs) - 1)]
            final_values.append(diffs[-1])
            if not any(diffs):
                break

        result += sum(final_values)

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
    input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    assert solve(input) == 114
