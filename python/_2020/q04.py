import re
import aocd


def part_one(batchfile: str) -> int:
    passports = [record for record in batchfile.split("\n\n")]
    required = {"byr:", "iyr:", "eyr:", "hgt:", "hcl:", "ecl:", "pid:"}
    return sum(all(field in passport for field in required) for passport in passports)


def part_two(batchfile: str) -> int:
    validator = re.compile(
        r"(?=.*\bbyr:(19[2-9]\d|200[0-2])\b)"
        r"(?=.*\biyr:(201\d|2020)\b)"
        r"(?=.*\beyr:(202\d|2030)\b)"
        r"(?=.*\bhgt:((1[5-8]\d|19[0-3])cm|(59|6\d|7[0-6])in)\b)"
        r"(?=.*\bhcl:(#[0-9a-f]{6})\b)"
        r"(?=.*\becl:(amb|blu|brn|gry|grn|hzl|oth)\b)"
        r"(?=.*\bpid:(\d{9})\b)"
    )
    return sum(
        bool(validator.match(record.replace("\n", " "))) for record in batchfile.split("\n\n")
    )


if __name__ == "__main__":
    batchfile = aocd.get_data(day=4, year=2020)
    print("Part 1: ", part_one(batchfile))
    print("Part 2: ", part_two(batchfile))
