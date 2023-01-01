import random
from typing import Protocol

import numpy as np


class Presenter(Protocol):
    def new_roboid_pos(self, pos: tuple[int, int]) -> None:
        ...

    def request_pos_value(self, pos: tuple[int, int]) -> float:
        ...

    def exploration_done(self, exploit_map: np.ndarray) -> None:
        ...

    def exploitation_done(self, walk_map: np.ndarray) -> None:
        ...


class Roboid:

    def __init__(self, presenter: Presenter, mapshape: tuple[int, int], pos_start: tuple[int, int]) -> None:
        self.presenter = presenter

        self.position = pos_start
        self.pos_start = pos_start
        self.pos_target = (0, 0)

        self.exploit_map = np.zeros(mapshape, dtype=np.float64)
        self.memory_map = np.zeros(mapshape, dtype=np.int64)
        self.walk_map = np.zeros(mapshape, dtype=np.float64)

        self.adjacent_pos = []

    # Getters and setters position

    def set_position(self, position: tuple[int, int]) -> None:
        """Set the current position.

        Args:
            position (tuple[int, int]): current position
        """
        self.position = position
        self.memory_map[position] += 1
        self.presenter.new_roboid_pos(position)

    def get_position(self) -> tuple[int, int]:
        """Get the current position.

        Returns:
            tuple[int, int]: current position
        """
        return self.position

    def set_start(self, position: tuple[int, int]) -> None:
        """Set the start position.

        Args:
            position (tuple[int, int]): start position

        Returns:
            None
        """
        self.pos_start = position

    def get_start(self) -> tuple[int, int]:
        """Get the start position.

        Returns:
            tuple[int, int]: start position
        """
        return self.pos_start

    def set_target(self, position: tuple[int, int]) -> None:
        """Set the target position.

        Args:
            position (tuple[int, int]): target position

        Returns:
            None
        """
        self.pos_target = position

    def get_target(self) -> tuple[int, int]:
        """Get the target position.

        Returns:
            tuple[int, int]: target position
        """
        return self.pos_target

    def set_adjacent_pos(self, positions: list[tuple[int, int]]) -> None:
        """Set the adjacent positions.

        Args:
            positions (list[tuple[int, int]]): adjacent positions

        Returns:
            None
        """
        self.adjacent_pos = positions

    def get_adjacent_pos(self) -> list[tuple[int, int]]:
        """Get the adjacent positions.

        Returns:
            list[tuple[int, int]]: adjacent positions
        """
        return self.adjacent_pos

    # Getters and setters maps

    def get_memory_map(self) -> np.ndarray:
        """Get the memory map.

        Returns:
            np.ndarray: memory map
        """
        return self.memory_map

    def get_exploit_map(self) -> np.ndarray:
        """Get the exploit map.

        Returns:
            np.ndarray: exploit map
        """
        return self.exploit_map

    # Checks

    def is_target(self) -> bool:
        """Check if the current position is the target position.

        Returns:
            bool: True if the current position is the target position
        """
        return self.position == self.pos_target

    def is_forbidden(self, position: tuple[int, int]) -> bool:
        """Check if the given position is forbidden.

        Args:
            position (tuple[int, int]): position to check

        Returns:
            bool: True if the given position is forbidden
        """
        x, y = position
        if x < 0 or y < 0:
            return True
        elif self.presenter.request_pos_value(position) < 0:
            return True

    # Actions positions

    def calc_adjacent_pos(self) -> None:
        """Calculate the adjacent positions.

        Returns:
            None
        """
        x, y = self.position
        adjacent_pos = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        adjacent_pos = [pos for pos in adjacent_pos if not self.is_forbidden(pos)]
        if not adjacent_pos:
            adjacent_pos = [self.position]
            print('Impossible to move, stay at the same position.')
        self.set_adjacent_pos(adjacent_pos)

    def choose_adjacent_pos(self) -> tuple[int, int]:
        """Choose a random adjacent position to the current position.

        Returns:
            tuple[int, int]: chosen position
        """
        return random.choice(self.adjacent_pos)

    def reset_pos(self) -> None:
        """Reset the current position to the start position.

        Returns:
            None
        """
        self.set_position(self.pos_start)

    # Actions maps

    def calc_exploit_map(self) -> None:
        """Calculate the exploit map.

        Returns:
            None
        """
        self.exploit_map = self.memory_map / self.memory_map.max()

    def wipe_exploit_map(self) -> None:
        """Wipe the exploit map.

        Returns:
            None
        """
        self.exploit_map = np.zeros(self.exploit_map.shape, dtype=np.float64)

    def wipe_memory_map(self) -> None:
        """Wipe the memory map.

        Returns:
            None
        """
        self.memory_map = np.zeros(self.memory_map.shape, dtype=np.int64)

    def wipe_walk_map(self) -> None:
        """Wipe the walk map.

        Returns:
            None
        """
        self.walk_map = np.zeros(self.walk_map.shape, dtype=np.float64)

    # Modi operandi

    def explore(self) -> None:
        """Explore the map.

        Returns:
            None
        """
        while not self.is_target():
            self.calc_adjacent_pos()
            self.set_position(self.choose_adjacent_pos())
        self.presenter.exploration_done(self.exploit_map)

    def exploit(self) -> None:
        """Exploit the map.

        Returns:
            None
        """
        while not self.is_target():
            self.calc_adjacent_pos()
            pos_walk: tuple[int, int]
            for index, pos in enumerate(self.adjacent_pos):
                if index == 0:
                    pos_walk = pos
                if self.exploit_map[pos] > self.exploit_map[pos_walk]:
                    pos_walk = pos
            self.walk_map[pos_walk] += 1
            self.set_position(pos_walk)
        self.presenter.exploitation_done(self.walk_map)
