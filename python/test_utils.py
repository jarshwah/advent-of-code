from textwrap import dedent

import pytest

from . import utils


class TestInput:
    def test_string(self):
        data = "abc"
        assert utils.Input(data).string == "abc"

    def test_integer(self):
        data = "123"
        assert utils.Input(data).integer == 123

    def test_number(self):
        data = "123"
        assert utils.Input(data).number == 123

    def test_float(self):
        data = "1.23"
        assert utils.Input(data).float == 1.23

    def test_scan_ints(self):
        data = "1 2 3"
        assert utils.Input(data).scan_ints() == [1, 2, 3]

    def test_parse(self):
        data = "oh hi there"
        parsed = utils.Input(data).parse("oh {} there")
        assert parsed[0] == "hi"

    def test_lines(self):
        data = dedent(
            """\
            abc
            123"""
        )
        lines = utils.Input(data).lines()
        assert lines.strings == ["abc", "123"]

    def test_columns(self):
        data = dedent(
            """\
            1   3
            8   2
            4   5"""
        )
        assert utils.Input(data).columns().numbers == [[1, 8, 4], [3, 2, 5]]

    def test_columns_wide(self):
        data = dedent(
            """\
            1   3   4
            8   2   5
            4   5   6"""
        )
        assert utils.Input(data).columns().numbers == [[1, 8, 4], [3, 2, 5], [4, 5, 6]]

    def test_split(self):
        data = "abc,123"
        assert utils.Input(data).split(",").strings == ["abc", "123"]

    def test_group(self):
        data = dedent(
            """\
            abc
            123

            def
            456"""
        )
        assert utils.Input(data).group().strings == [["abc", "123"], ["def", "456"]]

    def test_grid(self):
        data = dedent(
            """\
            a.b
            d.e
            ..f"""
        )
        grid = utils.Input(data).grid()
        assert grid[0, 0] == "a"
        assert grid[0, 1] == "."
        assert grid[0, 2] == "b"
        assert grid[1, 0] == "d"
        assert grid[1, 1] == "."
        assert grid[1, 2] == "e"
        assert grid[2, 0] == "."
        assert grid[2, 1] == "."
        assert grid[2, 2] == "f"
        assert len(grid) == 9

    def test_grid_int(self):
        data = dedent(
            """\
            123
            456
            789"""
        )
        grid = utils.Input(data).grid_int()
        assert grid[0, 0] == 1
        assert grid[0, 1] == 2
        assert grid[0, 2] == 3
        assert grid[1, 0] == 4
        assert grid[1, 1] == 5
        assert grid[1, 2] == 6
        assert grid[2, 0] == 7
        assert grid[2, 1] == 8
        assert grid[2, 2] == 9
        assert len(grid) == 9


class TestInputList:
    def test_strings(self):
        data = dedent(
            """\
            abc
            123"""
        )
        assert utils.Input(data).lines().strings == ["abc", "123"]

    def test_integers(self):
        data = dedent(
            """\
            123
            456"""
        )
        assert utils.Input(data).lines().integers == [123, 456]

    def test_floats(self):
        data = dedent(
            """\
            1.23
            4.56"""
        )
        assert utils.Input(data).lines().floats == [1.23, 4.56]

    def test_scan_ints(self):
        data = "1 2 3\n4 5 something 6"
        assert utils.Input(data).split("\n").scan_ints() == [[1, 2, 3], [4, 5, 6]]

    def test_parse(self):
        data = dedent(
            """\
            Game 1: a b c
            Game 2: d e f"""
        )
        results = utils.Input(data).lines().parse("Game {}: {} {} {}")
        a, b, c, d = results[0]
        assert [a, b, c, d] == ["1", "a", "b", "c"]
        a, b, c, d = results[1]
        assert [a, b, c, d] == ["2", "d", "e", "f"]

    def test_split(self):
        data = dedent(
            """\
            abc,123
            def,456"""
        )
        assert utils.Input(data).lines().split(",").strings == [["abc", "123"], ["def", "456"]]


class TestInputGroup:
    def test_strings(self):
        data = dedent(
            """\
            abc
            123

            def
            456"""
        )
        assert utils.Input(data).group().strings == [["abc", "123"], ["def", "456"]]

    def test_integers(self):
        data = dedent(
            """\
            123
            456

            789
            012"""
        )
        assert utils.Input(data).group().integers == [[123, 456], [789, 12]]

    def test_floats(self):
        data = dedent(
            """\
            1.23
            4.56

            7.89
            0.12"""
        )
        assert utils.Input(data).group().floats == [[1.23, 4.56], [7.89, 0.12]]

    def test_scan_ints(self):
        data = "1 2 3\n4 5 6\n\n7 8 9\n10 11 12"
        assert utils.Input(data).group("\n\n", "\n").scan_ints() == [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [10, 11, 12]],
        ]

    def test_parse(self):
        data = dedent(
            """\
            Game 1: a b c
            Game 1: d e f

            Game 2: g h i
            Game 2: j k l"""
        )
        results = utils.Input(data).group(sep="\n").parse("Game {}: {} {} {}")
        a, b, c, d = results[0][0]
        assert [a, b, c, d] == ["1", "a", "b", "c"]
        a, b, c, d = results[0][1]
        assert [a, b, c, d] == ["1", "d", "e", "f"]

        a, b, c, d = results[1][0]
        assert [a, b, c, d] == ["2", "g", "h", "i"]
        a, b, c, d = results[1][1]
        assert [a, b, c, d] == ["2", "j", "k", "l"]

    def test_grid(self):
        data = dedent(
            """\
            123
            456
            789"""
        )
        grid = utils.Input(data).group("\n").grid()
        assert grid[0, 0] == "1"
        assert grid[0, 1] == "2"
        assert grid[0, 2] == "3"
        assert grid[1, 0] == "4"
        assert grid[1, 1] == "5"
        assert grid[1, 2] == "6"
        assert grid[2, 0] == "7"
        assert grid[2, 1] == "8"
        assert grid[2, 2] == "9"
        assert len(grid) == 9

    def test_grid_int(self):
        data = dedent(
            """\
            123
            456
            789"""
        )
        grid = utils.Input(data).group("\n").grid_int()
        assert grid[0, 0] == 1
        assert grid[0, 1] == 2
        assert grid[0, 2] == 3
        assert grid[1, 0] == 4
        assert grid[1, 1] == 5
        assert grid[1, 2] == 6
        assert grid[2, 0] == 7
        assert grid[2, 1] == 8
        assert grid[2, 2] == 9
        assert len(grid) == 9


class TestGrid:
    def test_rows(self):
        data = dedent(
            """\
            abc
            123"""
        )
        grid = utils.Input(data).grid()
        rows = list(grid.rows())
        assert rows == [["a", "b", "c"], ["1", "2", "3"]]
        joined = ["".join(row) for row in rows]
        assert joined == ["abc", "123"]

    def test_cols(self):
        data = dedent(
            """\
            abc
            123"""
        )
        grid = utils.Input(data).grid()
        cols = list(grid.cols())
        assert cols == [["a", "1"], ["b", "2"], ["c", "3"]]
        joined = ["".join(col) for col in cols]
        assert joined == ["a1", "b2", "c3"]

    def test_strings(self):
        data = dedent(
            """\
            abc
            123"""
        )
        grid = utils.Input(data).grid()
        assert grid.strings() == ["abc", "123"]

    def test_hash_key(self):
        data = dedent(
            """\
            abc
            123"""
        )
        grid = utils.Input(data).grid()
        assert grid.hash_key() == "abc123"

    def test_rotate(self):
        data = dedent(
            """\
            abc
            123"""
        )
        grid = utils.Input(data).grid()
        assert grid.strings() == ["abc", "123"]
        grid = grid.rotate(1)
        assert grid.strings() == ["1a", "2b", "3c"]
        grid = grid.rotate(1)
        assert grid.strings() == ["321", "cba"]
        grid = grid.rotate(1)
        assert grid.strings() == ["c3", "b2", "a1"]
        grid = grid.rotate(1)
        assert grid.strings() == ["abc", "123"]
        grid = grid.rotate(2)
        assert grid.strings() == ["321", "cba"]
        grid = grid.rotate(-1)
        assert grid.strings() == ["1a", "2b", "3c"]

    def test_transpose(self):
        data = dedent(
            """\
            abc
            123"""
        )
        grid = utils.Input(data).grid()
        assert grid.strings() == ["abc", "123"]
        grid = grid.transpose()
        assert grid.strings() == ["a1", "b2", "c3"]
        grid = grid.transpose()
        assert grid.strings() == ["abc", "123"]


class TestRotate:
    def test_rotate_1(self):
        rows = ["abc", "123"]
        assert utils.rotate(rows, 1) == [list("1a"), list("2b"), list("3c")]
        assert utils.rotate(rows, 3) == [list("c3"), list("b2"), list("a1")]
        assert utils.rotate(rows, -1) == [list("c3"), list("b2"), list("a1")]


class TestShoelace:
    def test_area(self):
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        assert utils.shoelace(points) == 1

    def test_larger_area(self):
        # fmt: off
        points = [
            # They must be in order, this is going clockwise, but the points
            # are not in their actual location.
            (0, 0), (0, 1), (0, 2),
            (1, 2),         (0, 2),
            (2, 2), (2, 1), (2, 1),
        ]
        # fmt: on
        assert utils.shoelace(points) == 3 == utils.area_inside_boundary(points)

    def test_showlace_iter(self):
        # fmt: off
        points = [
            # They must be in order, this is going clockwise, but the points
            # are not in their actual location.
            (0, 0), (0, 1), (0, 2),
            (1, 2),         (0, 2),
            (2, 2), (2, 1), (2, 1),
        ]
        # fmt: on
        gen = utils.shoelace_iter(points[0])
        next(gen)
        for point in points[1:]:
            gen.send(point)
        area = next(gen)
        assert area == 3


class TestPointAdd:
    def test_add(self):
        assert utils.point_add((1, 2), (3, 4)) == (4, 6)

    def test_add_steps(self):
        assert utils.point_add((1, 2), (3, 4), 2) == (7, 10)


class TestScanInts:
    @pytest.mark.parametrize(
        "data,expected",
        [
            ("abc", []),
            ("123", [123]),
            ("-123", [-123]),
            ("1 2 3", [1, 2, 3]),
            ("1 -2 3", [1, -2, 3]),
            ("Some 1 numbers 2 found 3", [1, 2, 3]),
            ("Button A: 3 Button C: 5 And some more nonsense 7", [3, 5, 7]),
        ],
    )
    def test_numbers_found(self, data: str, expected: list[int]):
        assert utils.scan_ints(data) == expected
