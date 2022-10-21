#!/usr/bin/env python3.10
from dataclasses import dataclass
import math
from typing import Iterator
from typing_extensions import Self


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

    def __and__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x & other.x if isinstance(other, type(self)) else other,
            y=self.y & other.y if isinstance(other, type(self)) else other,
            z=self.z & other.z if isinstance(other, type(self)) else other)

    def __or__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x | other.x if isinstance(other, type(self)) else other,
            y=self.y | other.y if isinstance(other, type(self)) else other,
            z=self.z | other.z if isinstance(other, type(self)) else other)

    def __xor__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x ^ other.x if isinstance(other, type(self)) else other,
            y=self.y ^ other.y if isinstance(other, type(self)) else other,
            z=self.z ^ other.z if isinstance(other, type(self)) else other)

    def __mul__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x * other.x if isinstance(other, type(self)) else other,
            y=self.y * other.y if isinstance(other, type(self)) else other,
            z=self.z * other.z if isinstance(other, type(self)) else other)

    def __pow__(self, other: Self | int | float) -> Self:
        return Point(
            x=self.x ** other.x if isinstance(other, type(self)) else other,
            y=self.y ** other.y if isinstance(other, type(self)) else other,
            z=self.z ** other.z if isinstance(other, type(self)) else other)

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
            ret += coord
        return ret


if __name__ == "__main__":
    pass
