import sqlite3
import aocd


def part_one(db: sqlite3.Connection) -> int:
    """
    Example:
        2-9 c: ccccccccc
    """
    sql = """
    WITH parsed AS (
        SELECT
            cast(substr(
                password,
                0,
                instr(password, '-')
            ) as int) as low,
            cast(substr(
                password,
                instr(password, '-') + 1,
                instr(password, ' ') - instr(password, '-')
            ) as int) as high,
            substr(
                password,
                instr(password, ':') -1,
                1
            ) as letter,
            trim(substr(
                password,
                instr(password, ':') + 1
            )) as password
        FROM passwords
    ),
    occurences AS (
        SELECT
            (LENGTH(password) - LENGTH(REPLACE(password, letter, ''))) as counter,
            *
        FROM parsed
    )
    SELECT count(*)
    FROM occurences
    WHERE counter >= low AND counter <= high
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


def part_two(db: sqlite3.Connection) -> int:
    """
    Example:
        2-9 c: ccccccccc
    """
    sql = """
    WITH parsed AS (
        SELECT
            cast(substr(
                password,
                0,
                instr(password, '-')
            ) as int) as low,
            cast(substr(
                password,
                instr(password, '-') + 1,
                instr(password, ' ') - instr(password, '-')
            ) as int) as high,
            substr(
                password,
                instr(password, ':') -1,
                1
            ) as letter,
            trim(substr(
                password,
                instr(password, ':') + 1
            )) as password
        FROM passwords
    ),
    matcher AS (
        SELECT
            substr(password, low, 1) as first,
            substr(password, high, 1) as second,
            *
        FROM parsed
    )
    SELECT
        count(*)
    FROM matcher
    WHERE
         (first = letter) != (second = letter)
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE passwords (password text)")
    passwords = [
        [record]
        for record in aocd.get_data(day=2, year=2020).splitlines()
        if record.strip()
    ]
    db.executemany("INSERT INTO passwords values (?)", passwords)
    print("Part 1: ", part_one(db))
    print("Part 2: ", part_two(db))
