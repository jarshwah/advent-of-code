import re
import aocd


def part_one(batchfile: str) -> int:
    passports = [record.replace("\n", " ") for record in batchfile.split("\n\n")]
    required = {"byr:", "iyr:", "eyr:", "hgt:", "hcl:", "ecl:", "pid:"}
    return sum(all(field in passport for field in required) for passport in passports)


def part_two(batchfile: str) -> int:
    extractor = re.compile(
        r"^"
        r"(?=.*\bbyr:(?P<byr>\d{4})\b)"
        r"(?=.*\biyr:(?P<iyr>\d{4})\b)"
        r"(?=.*\beyr:(?P<eyr>\d{4})\b)"
        r"(?=.*\bhgt:(?P<hgt>\d{2,3})(?P<units>(cm|in))\b)"
        r"(?=.*\bhcl:(?P<hcl>#[0-9a-f]{6})\b)"
        r"(?=.*\becl:(?P<ecl>(amb|blu|brn|gry|grn|hzl|oth))\b)"
        r"(?=.*\bpid:(?P<pid>\d{9})\b)"
        r".*$"
    )
    valid = 0
    passports = [record.replace("\n", " ") for record in batchfile.split("\n\n")]
    for passport in passports:
        if (match := extractor.match(passport)) :
            parsed = match.groupdict()
            units = parsed["units"]
            valid += bool(
                1920 <= int(parsed["byr"]) <= 2002
                and 2010 <= int(parsed["iyr"]) <= 2020
                and 2020 <= int(parsed["eyr"]) <= 2030
                and (
                    (units == "cm" and (150 <= int(parsed["hgt"]) <= 193))
                    or (units == "in" and (59 <= int(parsed["hgt"]) <= 76))
                )
            )
    return valid


if __name__ == "__main__":
    batchfile = aocd.get_data(day=4, year=2020)
    print("Part 1: ", part_one(batchfile))
    print("Part 2: ", part_two(batchfile))
