#!/usr/bin/env python3.10
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Iterator
from typing_extensions import Self


@dataclass
class Matrix:
    x: list[float]
    y: list[float]
    z: list[float]

    def __and__(self, other: Self | Point) -> Self:
        return Matrix(
            x=self.x.extend(other.x) if isinstance(other, type(self)) else self.x.append(other.x),
            y=self.y.extend(other.y) if isinstance(other, type(self)) else self.y.append(other.y),
            z=self.z.extend(other.z) if isinstance(other, type(self)) else self.z.append(other.z))

    @staticmethod
    def extract_from_ptlist(pt_list: list[Point]) -> Self:
        ret = Matrix([], [], [])
        for pt in pt_list:
            ret = ret.__and__(pt)
        return ret


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

    def __and__(self, other: Self) -> Matrix:
        return Matrix(
            x=[self.x, other.x],
            y=[self.y, other.y],
            z=[self.z, other.z])

    def __mul__(self, other: Self | int | float) -> Matrix:
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
            y=self.y ** other.y if isinstance(other, type(self)) else self.x ** other,
            z=self.z ** other.z if isinstance(other, type(self)) else self.x ** other)

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


if __name__ == "__main__":
    pass
