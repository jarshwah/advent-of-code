import math
import sqlite3

import aocd


def part_one(db: sqlite3.Connection) -> int:
    sql = """
    WITH RECURSIVE attempts(attempt, game_num, time, distance) AS (
        -- This is producing lots of duplicates, fine tune..
        -- too slow for real input
        SELECT 1, 0, 0, 0
        UNION ALL
        SELECT DISTINCT attempt + 1, games.game_num, games.time, games.distance
        FROM games, attempts
        WHERE attempt < games.time
    )
    SELECT CAST(ROUND(EXP(SUM(LOG(num_wins)))) as int) FROM (
        SELECT COUNT(attempt) num_wins, game_num
        FROM (
            SELECT DISTINCT attempt, game_num
            FROM attempts
            WHERE game_num > 0
            AND attempt * (time - attempt) > distance
        ) wins
        GROUP BY game_num
    ) inn
    """
    # sql = """
    # WITH RECURSIVE attempts(attempt, game_num, time, distance) AS (
    #     -- This is producing lots of duplicates, fine tune..
    #     SELECT 1, 0, 0, 0
    #     UNION ALL
    #     SELECT DISTINCT attempt + 1, games.game_num, games.time, games.distance
    #     FROM games, attempts
    #     WHERE attempt < (games.time / 2)
    # )
    # SELECT CAST(ROUND(EXP(SUM(LOG(num_wins)))) as int) FROM (
    #     SELECT COUNT(attempt) * 2 - (time % 2) num_wins, game_num
    #     FROM (
    #         SELECT DISTINCT attempt, game_num, time
    #         FROM attempts
    #         WHERE game_num > 0
    #         AND attempt * (time - attempt) > distance
    #     ) wins
    #     GROUP BY game_num
    # ) inn
    # """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


# 1 2 3 [4 5 6] 7 8 9


def part_two(db: sqlite3.Connection) -> int:
    sql = """
    WITH RECURSIVE attempts(attempt, time, distance) AS (
        -- This is producing lots of duplicates, fine tune..
        SELECT 0, 0, 0
        UNION ALL
        SELECT attempt + 1, inn.time, inn.distance
        FROM (
            SELECT
                CAST(REPLACE(GROUP_CONCAT(games.time), ',','') as int) as time,
                CAST(REPLACE(GROUP_CONCAT(games.distance), ',', '') as int) as distance
            FROM games
        ) inn, attempts
        WHERE attempt < inn.time
    )
    SELECT COUNT(*) FROM (
        SELECT DISTINCT attempt, time, distance
        FROM attempts
        WHERE attempt * (time - attempt) > distance AND attempt > 0
    ) inn
    """
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.create_function("LOG", 1, math.log)
    db.create_function("EXP", 1, math.exp)
    db.execute("CREATE TABLE games (game_num int, time int, distance int)")

    test_data = """Time:      7  15   30
Distance:  9  40  200"""
    real_data = aocd.get_data(day=6, year=2023)
    games = zip(
        *[
            [int(n) for n in line.split(":")[1].split()]
            for line in real_data.splitlines()
        ]
    )
    numbered_games = [[idx + 1, *game] for idx, game in enumerate(games)]
    db.executemany("INSERT INTO games values (?, ?, ?)", numbered_games)
    # print("Part 1: ", part_one(db))
    print("Part 2: ", part_two(db))
