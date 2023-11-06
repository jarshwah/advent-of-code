import sqlite3

import aocd


def part_one(db: sqlite3.Connection) -> int:
    sql = """
    SELECT COUNT(*) FROM (
    SELECT
        depth,
        lead(depth) over (ORDER BY position) as next_depth
    FROM depths
    ) inn
    WHERE next_depth > depth
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


def part_two(db: sqlite3.Connection) -> int:
    sql = """
    SELECT COUNT(*) FROM (
    SELECT
        SUM(depth) over (ORDER BY position RANGE BETWEEN CURRENT ROW AND 2 FOLLOWING) depth,
        SUM(depth) over (ORDER BY position RANGE BETWEEN 1 FOLLOWING AND 3 FOLLOWING) next_depth
    FROM depths
    ) inn
    WHERE next_depth > depth
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE depths (depth int, position int)")
    depths = [
        [int(num), idx]
        for idx, num in enumerate(aocd.get_data(day=1, year=2021).splitlines())
    ]
    db.executemany("INSERT INTO depths values (?, ?)", depths)
    print("Part 1: ", part_one(db))
    print("Part 2: ", part_two(db))
