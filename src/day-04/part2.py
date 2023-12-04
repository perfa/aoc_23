from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Back, Fore, Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def solve(input):
    games = {}
    for game, number in zip(input.splitlines(), range(1, input.count("\n") + 2)):
        winners, given = game.split(": ")[1].split(" | ")
        winners = set(int(n) for n in winners.split())
        given = set(int(n) for n in given.split())
        matches = len(winners.intersection(given))
        games[number] = (1, matches)

    total = 0
    for number in sorted(games.keys()):
        count, matches = games[number]
        total += count

        if matches:
            won_cards = range(number + 1, number + matches + 1)
            for card in won_cards:
                old_count, matches = games[card]
                games[card] = (old_count + count, matches)
    return total


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    assert solve(input) == 30
