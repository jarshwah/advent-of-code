# advent-of-code

Python implementations for [Advent Of Code](https://adventofcode.com/) (and some SQL).

I use AOC as an opportunity to use the latest and greatest python features as well
as learning new libraries that I don't use in my day to day.

From the root directory each language I've used will have its own folder, and then
each of those will have a folder for each year I've participated.

Since running python files as both a module or a script is a pain, the shared
utils are symlinked into each year's folder.

The structure of most problems follows the pattern:

```python
def part_one(data: str):
    ...

def part_two(data: str):
    ...

def test():
    test_input = """ ... """
    assert part_one(test_input) == ...
    assert part_two(test_input) == ...

if __name__ == "__main__":
    test()
    data = aocd.get_data(day=1, year=2022)
    print(part_one(data))
    print(part_two(data))
```

The `aocd` library (advent-of-code-data) fetches the specific input for my account
via a token stored at `~/.config/aocd/token`. Grab the session token from a browser
session when logged in and populate that file.
