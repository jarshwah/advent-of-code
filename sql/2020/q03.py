import aocd
import math
import sqlite3


def part_one(db: sqlite3.Connection) -> int:
    sql = """
    SELECT count(*)
    FROM tiles
    WHERE tile = '#'
      AND x = (3 * y) % (SELECT count(*) FROM tiles WHERE y = 0)
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


def part_two(db: sqlite3.Connection) -> int:
    # There is no MUL() aggregate, but we can replicate it with exp(sum(log(val)))
    # https://blog.jooq.org/2018/09/21/how-to-write-a-multiplication-aggregate-function-in-sql/

    db.create_function("LOG", 1, math.log)
    db.create_function("EXP", 1, math.exp)

    sql = """
    WITH slopes AS (
        SELECT 1 as R, 1 as D
        UNION
        SELECT 3 as R, 1 as D
        UNION
        SELECT 5 as R, 1 as D
        UNION
        SELECT 7 as R, 1 as D
        UNION
        SELECT 1 as R, 2 as D
    )

    SELECT CAST(ROUND(EXP(SUM(LOG(trees)))) as int)
    FROM (
        SELECT
            count(*) trees
        FROM tiles
        CROSS JOIN slopes
        WHERE tile = '#'
        AND x = (R * (y/D)) % (SELECT count(*) FROM tiles WHERE y = 0)
        AND y % D = 0
        GROUP BY R, D
    ) inn
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE tiles (x int, y int, tile char)")
    lines = aocd.get_data(day=3, year=2020).splitlines()
    rows = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            rows.append((x, y, char))
    db.executemany("INSERT INTO tiles VALUES (?, ?, ?)", rows)
    print("Part 1: ", part_one(db))
    print("Part 2: ", part_two(db))
