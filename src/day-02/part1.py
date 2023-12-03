from collections import defaultdict
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem
BLOCKS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def solve(input):
    games = input.split("\n")
    solvable = []

    for game in games:
        name, outcomes = game.split(":")
        id_ = int(name.split(" ")[-1])
        solvable.append(id_)

        results = defaultdict(int)
        for outcome in outcomes.split("; "):
            for entry in outcome.split(", "):
                count, color = entry.strip().split(" ")
                results[color] = max(results[color], int(count))

        for color, top in results.items():
            if BLOCKS[color] < top:
                solvable.remove(id_)
                break

    return sum(solvable)


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    print(f"\t{result}\t{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    assert solve(input) == 8
