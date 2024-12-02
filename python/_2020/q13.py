import math
import typing as t
import aocd


def part_one(depart: int, buses: t.List[int]) -> int:
    return math.prod(min((bus - (depart % bus), bus) for bus in buses))


def part_two(buses: t.List[t.Tuple[int, int]]) -> int:
    # buses = [(7, 0), (13, 1), (59, 4), (31, 6), (19, 7)]
    t = 0
    combined_factor = 1
    for bus, offset in buses:
        # find each successive multiple, and skip ahead by the combined multiples to find the next
        while (t + offset) % bus != 0:
            t += combined_factor
        combined_factor *= bus
    # assert t == 1068781
    return t


if __name__ == "__main__":
    depart, timetable = aocd.get_data(day=13, year=2020).splitlines()
    buses = [int(bus) for bus in timetable.split(",") if bus != "x"]
    schedule = [(int(bus), idx) for idx, bus in enumerate(timetable.split(",")) if bus != "x"]
    print("Part 1: ", part_one(int(depart), buses))
    print("Part 2: ", part_two(schedule))
