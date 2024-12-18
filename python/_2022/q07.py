from __future__ import annotations

import typing as t
from dataclasses import dataclass, field
from functools import cached_property

import aocd


@dataclass
class File:
    size: int
    name: str


@dataclass
class Directory:
    name: str
    parent: Directory | None = None
    subdirs: dict[str, Directory] = field(default_factory=dict)
    files: dict[str, File] = field(default_factory=dict)

    def cd(self, dirname: str) -> Directory:
        if dirname == "..":
            return self.parent or self
        return self.subdirs.setdefault(dirname, Directory(name=dirname, parent=self))

    def file_found(self, filename: str, filesize: int) -> None:
        self.files.setdefault(filename, File(size=filesize, name=filename))

    @cached_property
    def size(self) -> int:
        return sum(f.size for f in self.files.values()) + sum(d.size for d in self.subdirs.values())

    def tree(self) -> t.Iterable[Directory]:
        yield self
        for subdir in self.subdirs.values():
            yield from subdir.tree()


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


def part_one(raw: str) -> int:
    root = parse_terminal(raw.splitlines())
    return sum(size_of for subdir in root.tree() if (size_of := subdir.size) <= 100000)


def part_two(raw: str) -> int:
    root = parse_terminal(raw.splitlines())
    consumed = root.size
    free = 70000000 - consumed
    target = 30000000 - free
    return min(size_of for subdir in root.tree() if (size_of := subdir.size) >= target)


def test():
    test_input = """$ cd /
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
7214296 k"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 95437, answer_1
    assert answer_2 == 24933642, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=7, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
