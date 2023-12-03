from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input2.txt").read()
identifier = Path(__file__).stem
numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}


def find_digit(line, p):
    c = line[p]
    if c.isdigit():
        return c

    for ordinal, num in numbers.items():
        if line[p:].startswith(ordinal):
            return num
    return 0


def solve(input):
    result = 0
    for line in input.split():
        p = 0
        digit = 0
        for p in range(len(line)):
            digit = find_digit(line, p)
            if digit:
                break
        result += 10 * int(digit)
        digit = 0
        for p in range(len(line) - 1, -1, -1):
            digit = find_digit(line, p)
            if digit:
                break
        result += int(digit)
    return result


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    print(f"\t{result}\t{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    assert solve(input) == 281
