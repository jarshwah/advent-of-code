import typing as t
import aocd


def solve_dict(data: t.List[int], target=2020) -> int:
    """
    Store last turn per spoken number in a dictionary

    Time: 8s
    """
    spoken = {num: turn for turn, num in enumerate(data, 1)}
    speak = -1
    for turn in range(len(data), target):
        last_spoken_turn = spoken.get(speak, turn)
        spoken[speak] = turn
        speak = turn - last_spoken_turn
    return speak


def solve_preallocate(data: t.List[int], target=2020) -> int:
    """
    Preallocate an array to avoid hash overhead.

    Time: 4s
    """
    spoken = [0] * target
    for turn, num in enumerate(data, 1):
        spoken[num] = turn
    speak = -1
    for turn in range(len(data), target):
        last_spoken_turn = spoken[speak] or turn
        spoken[speak] = turn
        speak = turn - last_spoken_turn
    return speak


if __name__ == "__main__":
    data = [int(num) for num in aocd.get_data(day=15, year=2020).split(",")]
    print("Part 1: ", solve_preallocate(data, 2020))
    print("Part 2: ", solve_preallocate(data, 30000000))
