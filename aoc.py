import os
from pathlib import Path

import click


@click.command
@click.option("--all", is_flag=True, default=False)
@click.option("--example", is_flag=True, default=False)
def main(all, example):
    print("Running AOC")
    print("===========")
    directories = sorted(Path(__file__).parent.glob("day-*"))
    if not all:
        directories = [directories[-1]]

    for directory in directories:
        print(directory.stem)
        print("-" * len(directory.stem))
        part1_path = directory / "part1.py"
        part2_path = directory / "part2.py"
        os.system(f"python {part1_path} {'--example' if example else ''}")
        os.system(f"python {part2_path} {'--example' if example else ''}")


if __name__ == "__main__":
    main()
