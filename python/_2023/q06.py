import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        games = zip(*[[int(n) for n in s.split(":")[1].split()] for s in input.lines().strings])
        game_wins = 1
        for time, record in games:
            wins = 0
            for attempt in range(1, time):
                would_be = attempt * (time - attempt)
                if would_be > record:
                    wins += 1
            game_wins *= wins
        return game_wins

    def part_two(self, input: utils.Input) -> str | int:
        time, distance = [int(s.split(":")[1].replace(" ", "")) for s in input.lines().strings]
        return sum(1 for attempt in range(1, time) if attempt * (time - attempt) > distance)


puzzle = Puzzle(
    year=2023,
    day=6,
    test_answers=("288", "71503"),
    test_input="""\
Time:      7  15   30
Distance:  9  40  200""",
)

if __name__ == "__main__":
    puzzle.cli()
