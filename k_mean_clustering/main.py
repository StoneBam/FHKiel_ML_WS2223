#!/usr/bin/env python3.10
import random

from point import Point


class RandomPointCloud(random.Random):

    def __init__(self, seed: str | int | None = None) -> None:
        super().__init__(seed)

    def create(self, n_pts: int, bounds: tuple[float, float], biases: tuple[float, float, float], dims: int = 2) -> list[Point]:
        return [Point(
            x=self.uniform(*bounds) + biases[0] if dims >= 1 else 0.0,
            y=self.uniform(*bounds) + biases[1] if dims >= 2 else 0.0,
            z=self.uniform(*bounds) + biases[2] if dims >= 3 else 0.0
            ) for _ in range(n_pts)]


if __name__ == '__main__':
    pass
