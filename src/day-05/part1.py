from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


class Range:
    def __init__(self, dest, origin, range):
        self._origin = origin
        self._dest = dest
        self._range = range

    def get(self, index):
        origin_offset = index - self._origin
        if origin_offset >= 0 and origin_offset < self._range:
            return self._dest + origin_offset
        return None


class RangeMap:
    def __init__(self, name):
        self._name = name
        self._ranges = []

    def add(self, range):
        self._ranges.append(range)

    def get(self, index):
        for range in self._ranges:
            res = range.get(index)
            if res:
                return res
        return index


def solve(input):
    data = input.splitlines()
    maps, map_ = [], None
    for line in data[2:]:
        if not line:
            maps.append(map_)
        elif ":" in line:
            map_ = RangeMap(line.split(":")[0])
        else:
            map_.add(Range(*[int(x) for x in line.split()]))
    maps.append(map_)

    seeds = [int(x) for x in data[0].split(":")[1].split()]
    locations = []
    for seed in seeds:
        x = seed
        for map_ in maps:
            x = map_.get(x)
        locations.append(x)

    return min(locations)

if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_range():
    r = Range(50, 98, 2)
    assert r.get(97) is None
    assert r.get(98) == 50
    assert r.get(99) == 51
    assert r.get(100) is None

def test_map():
    m = RangeMap("test")
    m.add(Range(50, 98, 2))
    m.add(Range(52, 50, 48))
    assert m.get(97) == 99
    assert m.get(98) == 50
    assert m.get(99) == 51
    assert m.get(79) == 81

def test_part1_example_1():
    input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    assert solve(input) == 35
