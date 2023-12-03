from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def is_symbol(c):
    return not c.isdigit() and c != "."


def symbol_near(rows, width, col_idx, row_idx):
    c_min = max(col_idx - 1, 0)
    c_max = min(col_idx + 1, width - 1)
    r_min = max(row_idx - 1, 0)
    r_max = min(row_idx + 1, len(rows) - 1)

    for col in range(c_min, c_max + 1):
        for row in range(r_min, r_max + 1):
            if col == col_idx and row == row_idx:
                continue

            if is_symbol(rows[row][col]):
                return True
    return False


def solve(input):
    rows = input.split("\n")
    width = len(rows[0])
    result = 0
    value = 0
    included = False

    for row_idx in range(len(rows)):
        if value and included:
            result += value

        row = rows[row_idx]
        included = False
        value = 0
        col_idx = 0
        while col_idx < width:
            if row[col_idx].isdigit():
                if not included:
                    included |= symbol_near(rows, width, col_idx, row_idx)
                value *= 10
                value += int(row[col_idx])
            elif value and included:
                result += value
                included = False
                value = 0
            else:
                included = False
                value = 0
            col_idx = col_idx + 1

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
    input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    assert solve(input) == 4361
