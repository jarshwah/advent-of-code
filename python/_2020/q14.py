import typing as t

import aocd
from parse import compile

parser = compile("mem[{address:d}] = {value:d}")


def part_one(data: t.List[str]) -> int:
    mask = "X" * 36
    memory = {}
    for instruction in data:
        if instruction.startswith("mask"):
            mask = instruction.removeprefix("mask = ")
            continue
        parsed = parser.parse(instruction).named
        address, bits = parsed["address"], list(bin(parsed["value"])[2:].zfill(36))
        for idx, bit in enumerate(mask):
            if bit == "X":
                continue
            bits[idx] = bit
        memory[address] = int("".join(bits), 2)
    return sum(memory.values())


def part_two(data: t.List[str]) -> int:
    memory = {}

    def gen_masks(mask: str) -> t.Iterable[str]:
        if "X" not in mask:
            yield mask
        else:
            yield from gen_masks(mask.replace("X", "0", 1))
            yield from gen_masks(mask.replace("X", "1", 1))

    masks = []
    for instruction in data:
        if instruction.startswith("mask"):
            # The address is unchanged with 0 EXCEPT if the 0 came from an X
            # so just replace 0 with Y and ignore Y later.
            masks = list(gen_masks(instruction.removeprefix("mask = ").replace("0", "Y")))
            continue
        parsed = parser.parse(instruction).named
        address, value = bin(parsed["address"])[2:].zfill(36), parsed["value"]
        addresses = []
        for mask in masks:
            masked_addr = list(address)
            for idx, bit in enumerate(mask):
                if bit == "Y":
                    continue
                masked_addr[idx] = bit
            addresses.append("".join(masked_addr))
        for addr in addresses:
            memory[int(addr, 2)] = value
    return sum(memory.values())


if __name__ == "__main__":
    data = aocd.get_data(day=14, year=2020).splitlines()
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
