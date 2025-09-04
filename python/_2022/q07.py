from __future__ import annotations
import typing as t
from dataclasses import dataclass, field
from functools import cached_property
import utils


def parse_terminal(lines: list[str]) -> Directory:
    root = Directory(name="/")
    cwd = root
    for line in lines:
        match line.split():
            case ["$", "cd", "/"]:
                cwd = root
            case ["$", "cd", dirname]:
                cwd = cwd.cd(dirname)
            case ["$", "ls"]:
                continue
            case ["dir", dirname]:
                continue
            case [filesize, filename]:
                cwd.file_found(filename, int(filesize))
            case _:
                raise ValueError(f"Command not understood: {line}")
    return root


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        root = parse_terminal(input.string.splitlines())
        return sum(size_of for subdir in root.tree() if (size_of := subdir.size) <= 100000)

    def part_two(self, input: utils.Input) -> str | int:
        root = parse_terminal(input.string.splitlines())
        consumed = root.size
        free = 70000000 - consumed
        target = 30000000 - free
        return min(size_of for subdir in root.tree() if (size_of := subdir.size) >= target)


puzzle = Puzzle(
    year=2022,
    day=7,
    test_answers=("95437", "24933642"),
    test_input="""\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""",
)

if __name__ == "__main__":
    puzzle.cli()
