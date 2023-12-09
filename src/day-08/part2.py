from functools import reduce
import re
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem
node_re = re.compile(r"(...) = \((...), (...)\)")


def factorize(number):
    factors = []
    factor = 2
    while number:
        if number % factor == 0:  # evenly divisible
            factors.append(factor)
            number /= factor
        else:
            factor += 1
            if factor > number:
                break
    return factors


def solve(input):
    lines = input.splitlines()
    instructions = lines[0]

    map = {}
    for line in lines[2:]:
        name, l, r = node_re.search(line).groups()
        map[name] = (l, r)

    starts = [name for name in map.keys() if name.endswith("A")]
    ends = []
    for start in starts:
        count = 0
        step = 0
        current = start
        while not current.endswith("Z"):
            current = map[current]["LR".index(instructions[step])]
            step = (step + 1) % len(instructions)
            count += 1
        ends.append(count)

    factors = set(sum([factorize(end) for end in ends], []))

    return reduce(lambda x, y: x * y, factors, 1)


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    assert solve(input) == 6


def test_part2_factorize():
    assert factorize(3) == [3]
    assert factorize(4) == [2, 2]
    assert factorize(9) == [3, 3]
    assert factorize(12) == [2, 2 ,3]
    assert factorize(20659) == [73, 283]
    assert factorize(20093) == [71, 283]
    assert factorize(14999) == [53, 283]  # aha.
