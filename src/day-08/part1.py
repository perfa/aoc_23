import re
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem
node_re = re.compile(r"(...) = \((...), (...)\)")


def solve(input):
    lines = input.splitlines()
    instructions = lines[0]

    map = {}
    for line in lines[2:]:
        name, l, r = node_re.search(line).groups()
        map[name] = (l, r)

    current = "AAA"
    step = 0
    count = 0
    while current != "ZZZ":
        if count > 2000000:
            break
        current = map[current]["LR".index(instructions[step])]
        step = (step + 1) % len(instructions)
        count += 1

    return count


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    assert solve(input) == 2


def test_part1_example_2():
    input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    assert solve(input) == 6
