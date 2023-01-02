import random
from typing import Callable

import numpy as np


class Roboid:

    def __init__(self, mapshape: tuple[int, int], pos_start: tuple[int, int], pos_target: tuple[int, int]) -> None:
        self.position = pos_start
        self.pos_start = pos_start
        self.pos_target = pos_target
        self.steps = 0
        self.num_explorations = 0

        self.mapshape = mapshape
        self.exploit_map = np.zeros(mapshape, dtype=np.float64)
        self.memory_map = np.zeros(mapshape, dtype=np.float64)
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
        self.steps += 1
        self.memory_map[position] = self.steps
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
        ret = {}
        for position in positions:
            if not self.is_forbidden(positions[position]):
                ret[position] = positions[position]
        if ret == {}:
            print("No adjacent position is available, staying at the same position")
            ret = {self.position: 0}
        self.adjacent_pos = ret

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

    def get_steps(self) -> int:
        """Get the number of steps.

        Returns:
            int: number of steps
        """
        return self.steps

    def get_explorations(self) -> int:
        """Get the number of explorations.

        Returns:
            int: number of explorations
        """
        return self.num_explorations

    # Checks

    def is_target(self) -> bool:
        """Check if the current position is the target position.

        Returns:
            bool: True if the current position is the target position
        """
        x, y = self.position
        x_target, y_target = self.pos_target
        ret = x == x_target and y == y_target
        if ret:
            return True
        return False

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

    def calc_manhattan_distance(self) -> float:
        """Calculate the Manhattan distance between the current position and the target position.

        Returns:
            float: Manhattan distance
        """
        x, y = self.pos_start
        x_target, y_target = self.pos_target
        return abs(x - x_target) + abs(y - y_target)

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
        self.steps = 0
        self.set_position(self.pos_start)

    # Actions maps

    def calc_exploit_map(self) -> None:
        """Calculate the exploit map.

        Returns:
            None
        """
        abs_exploit_map = self.exploit_map.sum()
        new_exploit_map = self.memory_map / self.memory_map.max()
        if (0 >= abs_exploit_map) or (abs_exploit_map > new_exploit_map.sum()):
            self.exploit_map = new_exploit_map

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

    def explore_once(self, adjacent_pos_func: Callable) -> np.ndarray:
        """Explore the map once.

        Args:
            adjacent_pos_func (Callable): function to calculate the adjacent positions

        Returns:
            self.exploit_map (np.ndarray): exploit map
        """

        # Setup
        self.wipe_memory_map()
        self.reset_pos()
        iteration_stop = (self.mapshape[0] * self.mapshape[1]) ** 3

        # Main loop
        while not self.is_target():
            adjacent_pos = self.calc_adjacent_pos_list()
            self.set_adjacent_pos(adjacent_pos_func(adjacent_pos))
            self.set_position(self.choose_adjacent_pos())

            if self.steps > iteration_stop:
                # Stop exploration if too many iterations
                print("Too many iterations, stopping exploration")
                break

        # Wrap up
        self.calc_exploit_map()
        return self.exploit_map

    def explore(self, adjacent_pos_func: Callable, explorations: int) -> np.ndarray:
        """Explore the map.

        Args:
            adjacent_pos_func (Callable): function to calculate the adjacent positions
            explorations (int): number of explorations

        Returns:
            self.exploit_map (np.ndarray): exploit map
        """
        self.num_explorations = 0
        while self.num_explorations < explorations:
            self.explore_once(adjacent_pos_func)
            if self.memory_map.max() <= self.calc_manhattan_distance():
                # Stop exploration min distance is reached
                print("Min distance reached, stopping exploration")
                break
            self.num_explorations += 1
        return self.exploit_map

    def exploit(self) -> np.ndarray:
        """Exploit the map.

        Returns:
            self.walk_map (np.ndarray): walk map
        """

        # Setup
        self.reset_pos()
        self.wipe_walk_map()
        iteration_stop = (self.mapshape[0] * self.mapshape[1])

        # Main loop
        print('Start exploiting the map')
        while not self.is_target():
            self.walk_map[self.position] = self.steps
            adjacent_pos = self.calc_adjacent_pos_list()
            exploit_value = 0
            exploit_pos = None
            for pos in adjacent_pos:
                if self.walk_map[pos] > 0:
                    continue
                if self.exploit_map[pos] > exploit_value:
                    exploit_value = self.exploit_map[pos]
                    exploit_pos = pos

            if exploit_pos is None:
                print('No adjacent position is available, stopping exploitation')
                break
            if self.steps > iteration_stop:
                print("Too many iterations, stopping exploitation")
                break

            self.set_position(exploit_pos)

        # Wrap up
        self.walk_map[self.position] = self.steps
        print('Arrived at the target position')
        self.wipe_memory_map()
        self.wipe_exploit_map()
        return self.walk_map
