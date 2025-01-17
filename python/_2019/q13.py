import itertools
import time
from enum import StrEnum

import intcode

import utils


class Tile(StrEnum):
    EMPTY = " "
    WALL = "+"
    BLOCK = "#"
    PADDLE = "="
    BALL = "O"


def to_tile(tile_id: int) -> Tile:
    match tile_id:
        case 0:
            return Tile.EMPTY
        case 1:
            return Tile.WALL
        case 2:
            return Tile.BLOCK
        case 3:
            return Tile.PADDLE
        case 4:
            return Tile.BALL
        case _:
            raise ValueError(tile_id)


class Puzzle(utils.Puzzle):
    """--- Day 13: Care Package ---"""

    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        program = list(input.split(",").numbers)

        # Startup!
        tiles = {}
        game = intcode.IntCode(program[::])
        output = game.run()
        for step in itertools.batched(output, 3, strict=True):
            xpos, ypos, tile_id = step
            tiles[(ypos, xpos)] = to_tile(tile_id)
        num_blocks = sum(1 for tile in tiles if tiles[tile] == Tile.BLOCK)

        # Let's play!
        program = [2] + program[1:]
        game = intcode.IntCode(program)
        grid = utils.Grid[Tile]([])
        grid.points = tiles
        ball = grid.find(Tile.BALL)
        paddle = grid.find(Tile.PADDLE)
        score = 0
        num_ticks = 0
        game.run()
        with grid.animate(False) as animator:
            while not game._halted:
                num_ticks += 1
                joystick = 0
                # AI: follow the ball.
                if ball[1] < paddle[1]:
                    joystick = -1
                elif ball[1] > paddle[1]:
                    joystick = 1

                game.input.write(joystick)

                # Tick. The game waits on input.
                while game.output._queue:
                    xpos, ypos, tile_id = next(game.output), next(game.output), next(game.output)
                    if xpos == -1 and ypos == 0:
                        score = tile_id
                        animator.set_header(f"Score: {score}")
                        continue

                    loc = (ypos, xpos)
                    tile = to_tile(tile_id)
                    grid[loc] = tile
                    if tile == Tile.BALL:
                        ball = loc
                    if tile == Tile.PADDLE:
                        paddle = loc

                if animator.animating:
                    animator.update(grid)
                    time.sleep(0.005)

        return num_blocks, score


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=13,
        both=True,
        no_tests=True,
        test_answers=("", ""),
        test_input="""""",
    )
    runner.cli()
