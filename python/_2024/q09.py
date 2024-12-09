from itertools import cycle

import utils


def compact(disk: list[int | None]) -> list[int | None]:
    """
    From right to left, move values into the left-most available space containing None.
    """
    NEW_SIZE = len(disk) - disk.count(None)
    DISK: list[int | None] = [None] * NEW_SIZE
    seek = len(disk) - 1
    for pos, val in enumerate(disk):
        if pos >= NEW_SIZE:
            # Full, stop.
            break

        if val is not None:
            DISK[pos] = val
            continue

        # Find the the next non-None value seeking backwards from the end
        while disk[seek] is None:
            seek -= 1
        DISK[pos] = disk[seek]
        seek -= 1
    return DISK


def checksum(disk: list[int | None]) -> int:
    """
    The checksum is the sum of pos*val for each value in the disk that is not None.
    """
    return sum(pos * val for pos, val in enumerate(disk) if val is not None)


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        The input is a list of numbers, alternating between file size and free space.

        Compact the disk by moving individual file parts right to left into empty space, then checksum it.
        """
        nums = list(map(int, list(input.data)))
        SIZE = sum(nums)
        DISK: list[int | None] = [None] * SIZE
        fp = 0
        for size, file_num, is_free in zip(nums, range(0, len(nums)), cycle([False, True])):
            if not is_free:
                DISK[fp : fp + size] = [file_num // 2] * size
            fp += size
        compacted = compact(DISK)
        return checksum(compacted)

    def part_two(self, input: utils.Input) -> str | int:
        """
        The input is a list of numbers, alternating between file size and free space.

        Compact the disk by moving whole files right to left into empty space, then checksum it.

        If a file can not be moved into empty space it remains where it is.
        """
        nums = list(map(int, list(input.data)))
        SIZE = sum(nums)
        DISK: list[int | None] = [None] * SIZE
        FREE_MAP: list[tuple[int, int]] = []
        DATA_MAP: list[tuple[int, int, int]] = []
        fp = 0
        for size, file_num, is_free in zip(nums, range(0, len(nums)), cycle([False, True])):
            if not is_free:
                DATA_MAP.append((size, fp, file_num // 2))
            elif size > 0:
                FREE_MAP.append((size, fp))
            fp += size

        # compact it - work from the reverse of DATA_MAP and attempt to fill the left of FREE_MAP
        for size, fp, val in reversed(DATA_MAP):
            try:
                free_map_idx, (free_size, free_fp) = utils.first(
                    (idx, (free_size, free_fp))
                    for idx, (free_size, free_fp) in enumerate(FREE_MAP)
                    if free_size >= size and free_fp <= fp
                )
            except StopIteration:
                # No free space large enough, leave it where it was
                DISK[fp : fp + size] = [val] * size
                continue

            DISK[free_fp : free_fp + size] = [val] * size
            if free_size == size:
                # Remove the free space so we don't check it again
                FREE_MAP.pop(free_map_idx)
            else:
                # Shrink the free space if there's some left
                FREE_MAP[free_map_idx] = (free_size - size, free_fp + size)

        return checksum(DISK)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=9,
        test_answers=("1928", "2858"),
        test_input="""2333133121414131402""",
    )
    runner.cli()
