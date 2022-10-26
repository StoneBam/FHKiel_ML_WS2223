#!/usr/bin/env python3.10
from dataclasses import dataclass
import math
from typing import Iterator, Self


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other: Self) -> Self:
        return Point(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return Point(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z)

    def __mul__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x * other.x if isinstance(other, type(self)) else self.x * other,
            y=self.y * other.y if isinstance(other, type(self)) else self.x * other,
            z=self.z * other.z if isinstance(other, type(self)) else self.x * other)

    def __truediv__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x / other.x if isinstance(other, type(self)) else self.x / other,
            y=self.y / other.y if isinstance(other, type(self)) else self.y / other,
            z=self.z / other.z if isinstance(other, type(self)) else self.z / other)

    def __pow__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x ** other.x if isinstance(other, type(self)) else self.x ** other,
            y=self.y ** other.y if isinstance(other, type(self)) else self.y ** other,
            z=self.z ** other.z if isinstance(other, type(self)) else self.z ** other)

    def __iter__(self) -> Iterator:
        for coord in (self.x, self.y, self.z):
            yield coord

    def distance(self, other: Self) -> float:
        temp = 0.0
        for coord in (other - self) ** 2:
            temp += coord
        return math.sqrt(temp)

    def distance_manhattan(self, other: Self) -> float:
        ret = 0.0
        for coord in (other - self):
            ret += abs(coord)
        return ret

    def round_display(self, digits: int = 2) -> tuple[float, float, float]:
        return round(self.x, digits), round(self.y, digits), round(self.z, digits)

    @staticmethod
    def extract_from_ptlist(pt_list: list[Self]) -> tuple:
        return list(zip(*[(*x,) for x in pt_list]))

    @staticmethod
    def subtract_elementwise_ptlist(pt_list_a: list[Self], pt_list_b: list[Self]) -> list[Self]:
        ret = []
        for a, b in zip(pt_list_a, pt_list_b):
            ret.append(a - b)
        return ret


if __name__ == "__main__":
    pass
