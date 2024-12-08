# Advent Of Code

Python implementations for [Advent Of Code](https://adventofcode.com/).

With some other languages, SQL for now, sprinkled throughout.

I use AOC as an opportunity to use the latest and greatest python features as well
as learning new libraries that I don't use in my day to day.

From the root directory each language I've used will have its own folder, and then
each of those will have a folder for each year I've participated.

Since running python files as both a module or a script is a pain, the shared
utils are symlinked into each year's folder.

The structure of most problems follows the pattern:

```python
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        ...

    def part_two(self, input: utils.Input) -> str | int:
        ...


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=1,
        test_answers=("1", "2"),
        test_input="""copied test input""",
    )
    runner.cli()
```

Which can be generated via:

```bash
$ cd python
$ uv run new_puzzle.py 1
```

There are a number of flags for running tests, specific parts, and alternate solutions.

```bash
$ uv run _2024/q01.py -1  # Run part one only
$ uv run _2024/q01.py -2  # Run part two
$ uv run _2024/q01.py -t  # Run tests only
$ uv run _2024/q01.py -a  # Run alternate solutions if they exist
$ uv run _2024/q01.py -12tfa  # Enable all flags at once
```

The `aocd` library (advent-of-code-data) fetches the specific input for my account
via a token stored at `~/.config/aocd/token`. Grab the session token from a browser
session when logged in and populate that file.
