from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def hash(input):
    current_value = 0
    for c in input:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def solve(input: str) -> int:
    return sum(hash(step) for step in input.split(","))


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = "HASH"
    assert solve(input) == 52


def test_part1_example_2():
    input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    assert solve(input) == 1320
