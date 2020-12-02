import sqlite3
import aocd


def part_one(db: sqlite3.Connection) -> int:
    sql = """
    SELECT e1.expense * e2.expense
    FROM expenses e1
    CROSS JOIN expenses e2
    WHERE e1.expense + e2.expense == 2020
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


def part_two(db: sqlite3.Connection) -> int:
    sql = """
    SELECT e1.expense * e2.expense * e3.expense
    FROM expenses e1
    CROSS JOIN expenses e2
    CROSS JOIN expenses e3
    WHERE e1.expense + e2.expense + e3.expense == 2020
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE expenses (expense int)")
    expenses = [[int(num)] for num in aocd.get_data(day=1, year=2020).splitlines() if num.strip()]
    db.executemany("INSERT INTO expenses values (?)", expenses)
    print("Part 1: ", part_one(db))
    print("Part 2: ", part_two(db))
