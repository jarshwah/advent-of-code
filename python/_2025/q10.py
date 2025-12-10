from collections import deque

import z3

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        pushes: list[int] = []
        for line in input.lines().strings:
            lights, *button_strings, _ = line.split()
            target = frozenset(pos for pos, state in enumerate(lights[1:-1]) if state == "#")
            buttons = [set(map(int, b[1:-1].split(","))) for b in button_strings]

            queue: deque[tuple[int, frozenset[int]]] = deque([(0, frozenset())])
            seen: set[frozenset[int]] = set()
            while queue:
                presses, current = queue.popleft()
                if current in seen:
                    continue
                seen.add(frozenset(current))

                if current == target:
                    pushes.append(presses)

                for move in buttons:
                    queue.append((presses + 1, current ^ move))
        return sum(pushes)

    def part_two(self, input: utils.Input) -> str | int:
        pushes: list[int] = []
        for line in input.lines().strings:
            _, *buttons_strings, joltage_string = line.split()
            joltages = [int(jolt) for jolt in joltage_string[1:-1].split(",")]
            buttons = [set(map(int, b[1:-1].split(","))) for b in buttons_strings]

            solver = z3.Optimize()
            presses = [z3.Int(f"press-{idx}") for idx in range(len(buttons))]
            press_count = z3.Int("press_count")
            solver.add(press_count == sum(presses))
            solver.add([press >= 0 for press in presses])
            for pos, jolt in enumerate(joltages):
                # Check jolt equal to button presses matching button
                solver.add(
                    jolt
                    == sum(
                        press for press, button_set in zip(presses, buttons) if pos in button_set
                    )
                )
            solver.minimize(press_count)
            solver.check()
            pushes.append(solver.model()[press_count].as_long())
        return sum(pushes)


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=10,
        test_answers=("7", "33"),
        test_input="""[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""",
    )
    runner.cli()
