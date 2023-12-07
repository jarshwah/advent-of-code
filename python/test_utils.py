from textwrap import dedent

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