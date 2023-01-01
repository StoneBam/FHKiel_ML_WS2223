import random
from typing import Callable

import numpy as np


class Roboid:

    def __init__(self, mapshape: tuple[int, int], pos_start: tuple[int, int]) -> None:
        self.position = pos_start
        self.pos_start = pos_start
        self.pos_target = (0, 0)

        self.exploit_map = np.zeros(mapshape, dtype=np.float64)
        self.memory_map = np.zeros(mapshape, dtype=np.int64)
        self.walk_map = np.zeros(mapshape, dtype=np.float64)

        self.adjacent_pos = {}

    # Getters and setters position

    def set_position(self, position: tuple[int, int]) -> tuple[int, int]:
        """Set the current position.

        Args:
            position (tuple[int, int]): current position

        Returns:
            tuple[int, int]: new position
        """
        self.position = position
        self.memory_map[position] += 1
        return position

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

    def set_adjacent_pos(self, positions: dict[tuple[int, int]: float]) -> None:
        """Set the adjacent positions.

        Args:
            positions (dict[tuple[int, int]: float]): adjacent positions

        Returns:
            None
        """
        for position in positions:
            if self.is_forbidden(positions[position]):
                del positions[position]
        if positions == {}:
            print("No adjacent position is available, staying at the same position")
            positions = {self.position: 0}
        self.adjacent_pos = positions

    def get_adjacent_pos(self) -> dict[tuple[int, int]: float]:
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

    def is_forbidden(self, pos_value: float) -> bool:
        """Check if the given position is forbidden.

        Args:
            pos_value (float): value of the given position

        Returns:
            bool: True if the given position is forbidden
        """
        return pos_value < 0

    # Actions positions

    def calc_adjacent_pos_list(self) -> list[tuple[int, int]]:
        """Calculate the adjacent positions.

        Returns:
            list[tuple[int, int]]: adjacent positions
        """
        x, y = self.position
        positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for pos in positions:
            if pos[0] < 0 or pos[1] < 0:
                positions.remove(pos)
        return positions

    def choose_adjacent_pos(self) -> tuple[int, int]:
        """Choose a random adjacent position to the current position.

        Returns:
            tuple[int, int]: chosen position
        """
        return random.choice(list(self.adjacent_pos))

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

    def wipe_maps(self) -> None:
        """Wipe all maps.

        Returns:
            None
        """
        self.wipe_exploit_map()
        self.wipe_memory_map()
        self.wipe_walk_map()

    # Modi operandi

    def explore(self, adjacent_pos_func: Callable) -> np.ndarray:
        """Explore the map.

        Returns:
            self.exploit_map (np.ndarray): exploit map
        """
        while not self.is_target():
            adjacent_pos = self.calc_adjacent_pos_list()
            self.set_adjacent_pos(adjacent_pos_func(adjacent_pos))
            self.set_position(self.choose_adjacent_pos())
        return self.exploit_map

    def exploit(self) -> np.ndarray:
        """Exploit the map.

        Returns:
            self.walk_map (np.ndarray): walk map
        """
        while not self.is_target():
            adjacent_pos = self.calc_adjacent_pos_list(self.position)
            pos_walk: tuple[int, int]
            for index, pos in enumerate(adjacent_pos):
                if index == 0:
                    pos_walk = pos
                if self.exploit_map[pos] > self.exploit_map[pos_walk]:
                    pos_walk = pos
            self.walk_map[pos_walk] += 1
            self.set_position(pos_walk)
        return self.walk_map
