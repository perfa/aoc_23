import re
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


def score(box: list[list[str, int]], box_id):
    result = 0
    for idx, [_, focal_length] in enumerate(box):
        result += (box_id + 1) * (idx + 1) * focal_length

    return result


def solve(input: str) -> int:
    boxes = [list() for _ in range(256)]

    for step in input.split(","):
        label, op, focal_length = re.search(r"(.+)([-=])([1-9]?)", step).groups()
        box = hash(label)
        done = False
        lens = 0
        while lens < len(boxes[box]):
            if boxes[box][lens][0] == label:
                match op:
                    case "=":
                        boxes[box][lens][1] = int(focal_length)
                        done = True
                    case "-":
                        del boxes[box][lens]
                        lens -= 1
                        done = True
            lens += 1
        if not done and op == "=":
            boxes[box].append([label, int(focal_length)])

    return sum(score(box, idx) for idx, box in enumerate(boxes))

if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    assert solve(input) == 145
