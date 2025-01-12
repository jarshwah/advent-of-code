import itertools
import operator
from functools import partial

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        W = 25
        H = 6
        if self.testing:
            H = 3
            W = 2
        SZ = W * H
        zeroes = int(1e9)
        ans = 0
        for layer in itertools.batched([int(s) for char in input.string for s in char], SZ):
            if (num_zeroes := layer.count(0)) < zeroes:
                zeroes = num_zeroes
                ans = layer.count(1) * layer.count(2)
        return ans

    def part_two(self, input: utils.Input) -> str | int:
        W = 25
        H = 6
        if self.testing:
            return ""
        SZ = W * H
        BLACK = 0
        WHITE = 1
        TRANSPARENT = 2
        TRANSLATE = {BLACK: " ", WHITE: "#"}

        layers = list(itertools.batched([int(s) for char in input.string for s in char], SZ))
        pixels = utils.transpose(layers)
        image = []
        for pixel_layers in pixels:
            colour = next(itertools.dropwhile(partial(operator.eq, TRANSPARENT), pixel_layers))
            image.append(colour)

        message = "".join(
            [TRANSLATE[px] + ("\n" if pn % W == 0 else "") for pn, px in enumerate(image)]
        )
        return message


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=8,
        test_answers=("1", ""),
        test_input="""123456789012""",
    )
    runner.cli()
