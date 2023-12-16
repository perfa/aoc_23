from pathlib import Path
from resource import RUSAGE_SELF, getrusage
from time import perf_counter

from colorama import Style, init

init()
input = open(Path(__file__).parent / "input.txt").read()
identifier = Path(__file__).stem


def out_of_bounds(x, y, width, height):
    return x >= width or y >= height or x < 0 or y < 0


def solve(input):
    map = input.splitlines()
    width, height = len(map[0]), len(map)

    maximum = 0
    for y in range(height):
        maximum = max(maximum, count_energized([1, 0], [0, y], map, width, height))
        maximum = max(maximum, count_energized([-1, 0], [width - 1, y], map, width, height))
    for x in range(width):
        maximum = max(maximum, count_energized([0, 1], [x, 0], map, width, height))
        maximum = max(maximum, count_energized([0, -1], [x, height - 1], map, width, height))

    return maximum


def count_energized(initial_direction, initial_position, map, width, height):
    beams = [(initial_position, initial_direction)]
    beam_lines = set()
    while beams:
        [x, y], [dir_x, dir_y] = beams.pop(0)
        if out_of_bounds(x, y, width, height):
            continue
        if (x, y, dir_x, dir_y) in beam_lines:
            continue
        beam_lines.add((x, y, dir_x, dir_y))
        match map[y][x]:
            case ".":
                beams.append(([x + dir_x, y + dir_y], [dir_x, dir_y]))
            case "/":
                match [dir_x, dir_y]:
                    case 1, 0:
                        beams.append(([x, y - 1], [0, -1]))
                    case -1, 0:
                        beams.append(([x , y + 1], [0, 1]))
                    case 0, 1:
                        beams.append(([x - 1, y], [-1, 0]))
                    case 0, -1:
                        beams.append(([x + 1, y], [1, 0]))
            case "\\":
                match [dir_x, dir_y]:
                    case 1, 0:
                        beams.append(([x, y + 1], [0, 1]))
                    case -1, 0:
                        beams.append(([x , y - 1], [0, -1]))
                    case 0, 1:
                        beams.append(([x + 1, y], [1, 0]))
                    case 0, -1:
                        beams.append(([x - 1, y], [-1, 0]))
            case "|":
                match [dir_x, dir_y]:
                    case _, 0:
                        beams.append(([x , y + 1], [0, 1]))
                        beams.append(([x , y - 1], [0, -1]))
                    case 0, _:
                        beams.append(([x + dir_x, y + dir_y], [dir_x, dir_y]))
            case "-":
                match [dir_x, dir_y]:
                    case 0, _:
                        beams.append(([x + 1, y], [1, 0]))
                        beams.append(([x - 1, y], [-1, 0]))
                    case _, 0:
                        beams.append(([x + dir_x, y + dir_y], [dir_x, dir_y]))
    energized = set([(x, y) for x, y, _, _ in beam_lines])
    return len(energized)


if __name__ == "__main__":
    print(f"{identifier}:", end="", flush=True)
    start = perf_counter()
    result = solve(input)
    elapsed = perf_counter() - start
    max_rss = getrusage(RUSAGE_SELF)[2] / 1024 / 1024

    result = str(result).ljust(20)
    print(f"\t{result}{Style.DIM}{elapsed:0.3f}s {max_rss:0.3f} MAX_RSS{Style.RESET_ALL}")


def test_part2_example_1():
    input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    assert solve(input) == 51
