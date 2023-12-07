from functools import reduce
from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem
values = "23456789TJQKA"

def solve(input):
    hands = []
    for line in input.splitlines():
        hand, bet = line.split()
        counts = [hand.count(c) for c in set(hand)]
        unique_cards = len(counts)

        match unique_cards:
            case 1:
                strength = 7
            case 2:
                if 4 in counts:
                    strength = 6
                else:
                    strength = 5  # full house
            case 3:
                if 3 in counts:
                    strength = 4
                else:
                    strength = 3  # 2 pair
            case 4:
                strength = 2
            case _:
                strength = 1

        strength_key = (
            (strength * 1000000000000) +
            (values.index(hand[0]) * 1000000000) +
            (values.index(hand[1]) * 10000000) +
            (values.index(hand[2]) * 100000) +
            (values.index(hand[3]) * 1000) +
            (values.index(hand[4]) * 10)
        )
        hands.append((strength_key, hand, int(bet)))

    hands.sort(key=lambda x: x[0])
    return reduce(
        lambda total, x: total + (x[1] * x[0]),
        zip(range(1, len(hands) + 1), [hand[-1] for hand in hands]),
        0
    )


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part1_example_1():
    input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    assert solve(input) == 6440
