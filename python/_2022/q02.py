import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        data = utils.Input.group("\n").strings
        score = 0
        for opponent, us in data:
            them, ours = table[opponent], table[us]
            if them == ours:  # draw
                score += 3 + ours
                continue
            elif (ours - them) % 3 == 1:  # win
                score += 6 + ours
                continue
            score += ours  # lose
        return score

    def part_two(self, input: utils.Input) -> str | int:
        data = utils.Input.group("\n").strings
        score = 0
        for opponent, us in data:
            them, ours = table[opponent], table[us]
            if ours == 2:  # draw
                score += 3 + them
                continue
            elif ours == 1:  # lose
                score += (them - 1) or 3
                continue
            score += (1 if them == 3 else them + 1) + 6  # win
        return score


puzzle = Puzzle(
    year=2022,
    day=2,
    test_answers=("15", "12"),
    test_input="""\
A Y
B X
C Z""",
)

if __name__ == "__main__":
    puzzle.cli()
