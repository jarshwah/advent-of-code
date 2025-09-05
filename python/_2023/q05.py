import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        data = input.group(sep="\n").strings
        locations = {}
        seeds = [int(seed) for line in data[0] for seed in line.split(":")[1].split()]
        for seed in seeds:
            current_src = seed
            for maps in data[1:]:
                for line in maps[1:]:
                    dst, src, cnt = [int(num) for num in line.split()]
                    if not (src <= current_src <= src + cnt - 1):
                        continue
                    current_src = dst + (current_src - src)
                    break
            locations[seed] = current_src
        return min(locations.values())

    def part_two(self, input: utils.Input) -> str | int:
        # Brute force :(
        # 8 minutes with python 3
        # 26 seconds with pypy3
        data = input.group(sep="\n").strings
        seeds = [int(seed) for line in data[0] for seed in line.split(":")[1].split()]

        seed_ranges = list(zip(seeds[0::2], seeds[1::2]))

        def valid_seed(seed: int) -> bool:
            return any(
                seed_start <= seed <= seed_start + seed_count - 1
                for seed_start, seed_count in seed_ranges
            )

        map_groups = []
        for maps in data[1:]:
            map_groups.append([tuple([int(num) for num in line.split()]) for line in maps[1:]])

        # Start from a reasonable value for testing
        start_from = 50_000_000 if not self.testing else 1

        for location in range(start_from, 1_000_000_000):
            current_src = location
            for maps in map_groups[::-1]:
                for dst, src, cnt in maps:
                    if not (dst <= current_src <= dst + cnt - 1):
                        continue
                    current_src = src + (current_src - dst)
                    break
            if valid_seed(current_src):
                return location


puzzle = Puzzle(
    year=2023,
    day=5,
    test_answers=("35", "46"),
    test_input="""seeds: 79 14 55 13

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
56 93 4""",
)

if __name__ == "__main__":
    puzzle.cli()
