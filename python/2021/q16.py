import math

import aocd


def partition(bits: str, idx: int) -> tuple[str, str]:
    return bits[:idx], bits[idx:]


def parse(data: str) -> None:
    versions = 0
    bits = bin(int(data, 16))[2:].zfill(len(data) * 4)

    def parse_packets(bits) -> tuple[int, str]:
        nonlocal versions
        if not bits or int(bits, 2) == 0:
            return 0, ""

        version, type_id, bits = bits[:3], int(bits[3:6], 2), bits[6:]
        versions += int(version, 2)
        if type_id == 4:  # literal
            literal = ""
            while True:
                parity, chunk = partition(bits, 1)
                chunk, bits = partition(chunk, 4)
                literal += chunk
                if parity == "0":
                    break
            return int(literal, 2), bits
        else:
            packets = []
            length_type_id, bits = partition(bits, 1)
            if length_type_id == "0":
                stlength, bits = partition(bits, 15)
                tlength = int(stlength, 2)
                subpackets, bits = partition(bits, tlength)
                while subpackets:
                    val, subpackets = parse_packets(subpackets)
                    packets.append(val)
            else:
                spackets, bits = partition(bits, 11)
                npackets = int(spackets, 2)
                for _ in range(npackets):
                    val, bits = parse_packets(bits)
                    packets.append(val)

            match type_id:
                case 0: return sum(packets), bits
                case 1: return math.prod(packets), bits
                case 2: return min(packets), bits
                case 3: return max(packets), bits
                case 5: return (packets[0] > packets[1]), bits
                case 6: return (packets[0] < packets[1]), bits
                case 7: return (packets[0] == packets[1]), bits
                case _: raise ValueError(type_id)

    val, bits = parse_packets(bits)
    return versions, val


def test():
    p1_1, _ = parse("8A004A801A8002F478")
    assert p1_1 == 16
    p1_2, _ = parse("620080001611562C8802118E34")
    assert p1_2 == 12
    p1_3, _ = parse("A0016C880162017C3686B18A3D4780")
    assert p1_3 == 31

    _, p2_1 = parse("C200B40A82")
    assert p2_1 == 3, p2_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=16, year=2021)
    p1, p2 = parse(data)
    print("Part 1: ", p1)
    print("Part 2: ", p2)
