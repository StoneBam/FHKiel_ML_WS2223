import random
from typing import Callable

import numpy as np


class Roboid:

    def __init__(self, mapshape: tuple[int, int], start: tuple[int, int] = None, target: tuple[int, int] = None) -> None:
        self.mapshape = mapshape
        if start is not None:
            self.start = start
        else:
            self.set_random_start()
        if target is not None:
            self.target = target
        else:
            self.set_random_target()
        self.position = self.start

        self._steps = 0
        self._num_explorations = 0

        self.exploit_map = np.zeros(mapshape, dtype=np.float64)
        self.memory_map = np.zeros(mapshape, dtype=np.float64)
        self.walk_map = np.zeros(mapshape, dtype=np.float64)

        self.adjacent_pos = {}
        self.pos_check = None

    @property
    def pos_check(self) -> Callable[[tuple[int, int]], float]:
        """Get the position check function.

        Returns:
            Callable[[tuple[int, int]], float]: position check function
        """
        return self._pos_check

    @pos_check.setter
    def pos_check(self, pos_check: Callable[[tuple[int, int]], float]) -> None:
        """Set the position check function.

        Args:
            pos_check (Callable[[tuple[int, int]], float]): position check function

        Returns:
            None
        """
        self._pos_check = pos_check

    @property
    def mapshape(self) -> tuple[int, int]:
        """Get the map shape.

        Returns:
            tuple[int, int]: map shape
        """
        return self._mapshape

    @mapshape.setter
    def mapshape(self, mapshape: tuple[int, int]) -> None:
        """Set the map shape.

        Args:
            mapshape (tuple[int, int]): map shape

        Returns:
            None
        """
        if mapshape[0] < 0 or mapshape[1] < 0:
            raise ValueError("Map shape must be positive.")
        if mapshape[0] < 4 or mapshape[1] < 4:
            raise ValueError("Map shape must be at least 4x4.")
        self._mapshape = mapshape

    @property
    def position(self) -> tuple[int, int]:
        """Get the current position.

        Returns:
            tuple[int, int]: current position
        """
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        """Set the current position.

        Args:
            position (tuple[int, int]): current position

        Returns:
            None
        """
        self.check_pos_is_valid(position)
        self._position = position

    @property
    def start(self) -> tuple[int, int]:
        """Get the start position.

        Returns:
            tuple[int, int]: start position
        """
        return self._start

    @start.setter
    def start(self, start: tuple[int, int]) -> None:
        """Set the start position.

        Args:
            start (tuple[int, int]): start position

        Returns:
            None
        """
        self.check_pos_is_valid(start)
        self._start = start

    @property
    def target(self) -> tuple[int, int]:
        """Get the target position.

        Returns:
            tuple[int, int]: target position
        """
        return self._target

    @target.setter
    def target(self, target: tuple[int, int]) -> None:
        """Set the target position.

        Args:
            target (tuple[int, int]): target position

        Returns:
            None
        """
        self.check_pos_is_valid(target)
        self._target = target

    @property
    def adjacent_pos(self) -> dict[tuple[int, int]: float]:
        """Get the adjacent positions.

        Returns:
            dict[tuple[int, int]: float]: adjacent positions
        """
        return self._adjacent_pos

    @adjacent_pos.setter
    def adjacent_pos(self, adjacent_pos: dict[tuple[int, int]: float]) -> None:
        """Set the adjacent positions.

        Args:
            adjacent_pos (dict[tuple[int, int]: float]): adjacent positions

        Returns:
            None
        """
        ret = {}
        for position in adjacent_pos:
            if not self.is_forbidden(adjacent_pos[position]):
                ret[position] = adjacent_pos[position]
        if ret == {}:
            print("No adjacent position is available, staying at the same position")
            ret = {self.position: 0}
        self._adjacent_pos = ret

    @property
    def steps(self) -> int:
        """Get the number of steps.

        Returns:
            int: number of steps
        """
        return self._steps

    @steps.setter
    def steps(self, steps: int) -> None:
        """Set the number of steps.

        Args:
            steps (int): number of steps

        Returns:
            None
        """
        if steps < 0:
            raise ValueError("Number of steps must be positive.")
        self._steps = steps

    @property
    def num_explorations(self) -> int:
        """Get the number of explorations.

        Returns:
            int: number of explorations
        """
        return self._num_explorations

    @num_explorations.setter
    def num_explorations(self, num_explorations: int) -> None:
        """Set the number of explorations.

        Args:
            num_explorations (int): number of explorations

        Returns:
            None
        """
        if num_explorations < 0:
            raise ValueError("Number of explorations must be positive.")
        self._num_explorations = num_explorations

    # Random start and target

    def set_random_start(self) -> None:
        """Set a random start position.

        Returns:
            None
        """
        start = (
            random.choice([i for i in range(1, self.mapshape[0] - 1)]),
            random.choice([i for i in range(1, self.mapshape[1] - 1)])
        )
        self.start = start
        self.position = start

    def set_random_target(self) -> None:
        """Set a random target position.

        Returns:
            None
        """
        # Make sure that the target position is not the same as the start position
        target = (
            random.choice([i for i in range(1, self.mapshape[0] - 1) if self.start[0] != i]),
            random.choice([i for i in range(1, self.mapshape[1] - 1) if self.start[1] != i])
        )
        self.target = target

    def set_random_start_and_target(self) -> None:
        """Set a random start and target position.

        Returns:
            None
        """
        self.set_random_start()
        self.set_random_target()

    # Getters and setters maps

    @property
    def memory_map(self) -> np.ndarray:
        """Get the memory map.

        Returns:
            np.ndarray: memory map
        """
        return self._memory_map

    @memory_map.setter
    def memory_map(self, memory_map: np.ndarray) -> None:
        """Set the memory map.

        Args:
            memory_map (np.ndarray): memory map

        Returns:
            None
        """
        self.check_map_is_valid(memory_map)
        self._memory_map = memory_map

    @property
    def exploit_map(self) -> np.ndarray:
        """Get the exploit map.

        Returns:
            np.ndarray: exploit map
        """
        return self._exploit_map

    @exploit_map.setter
    def exploit_map(self, exploit_map: np.ndarray) -> None:
        """Set the exploit map.

        Args:
            exploit_map (np.ndarray): exploit map

        Returns:
            None
        """
        self.check_map_is_valid(exploit_map)
        self._exploit_map = exploit_map

    @property
    def walk_map(self) -> np.ndarray:
        """Get the walk map.

        Returns:
            np.ndarray: walk map
        """
        return self._walk_map

    @walk_map.setter
    def walk_map(self, walk_map: np.ndarray) -> None:
        """Set the walk map.

        Args:
            walk_map (np.ndarray): walk map

        Returns:
            None
        """
        self.check_map_is_valid(walk_map)
        self._walk_map = walk_map

    # Checks

    def is_target(self) -> bool:
        """Check if the current position is the target position.

        Returns:
            bool: True if the current position is the target position
        """
        x, y = self.position
        x_target, y_target = self.target
        return x == x_target and y == y_target

    def is_forbidden(self, pos_value: float) -> bool:
        """Check if the given position is forbidden.

        Args:
            pos_value (float): value of the given position

        Returns:
            bool: True if the given position is forbidden
        """
        return pos_value < 0

    def is_curr_pos_valid(self) -> None:
        """Check if the current position is valid.

        Returns:
            None
        """
        if self.pos_check is None:
            raise ValueError("pos_check must be defined.")
        if self.is_forbidden(self.pos_check(self.position)):
            raise ValueError("Current position is forbidden.")

    def check_start_and_target(self) -> None:
        """Check if the start and target positions are valid.

        Args:
            pos_check (Callable[[tuple[int, int]], float]): function to check the position

        Returns:
            None
        """
        if self.pos_check is None:
            raise ValueError("pos_check must be defined.")
        if self.is_forbidden(self.pos_check(self.start)):
            self.set_random_start()
            return self.check_start_and_target()
        if self.is_forbidden(self.pos_check(self.target)):
            self.set_random_target()
            return self.check_start_and_target()

    def check_pos_is_valid(self, pos: tuple[int, int]) -> None:
        """Check if the given position is valid.

        Args:
            pos (tuple[int, int]): position to check

        Returns:
            None

        Raises:
            ValueError: if the position is not valid
        """
        x, y = pos
        if not (0 <= x < self.mapshape[0] and 0 <= y < self.mapshape[1]):
            raise ValueError("Position is not valid.")

    def check_map_is_valid(self, map: np.ndarray) -> None:
        """Check if the given map is valid.

        Args:
            map (np.ndarray): map to check

        Returns:
            None

        Raises:
            ValueError: if the map is not valid
        """
        if map.shape != self.mapshape:
            raise ValueError("Map is not valid.")

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
        x, y = self.start
        x_target, y_target = self.target
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
        self.position = self.start

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
        iteration_stop = (self.mapshape[0] * self.mapshape[1]) ** 2

        # Main loop
        while not self.is_target():
            adjacent_pos = self.calc_adjacent_pos_list()
            self.adjacent_pos = adjacent_pos_func(adjacent_pos)
            self.position = self.choose_adjacent_pos()
            self.steps += 1
            self.memory_map[self.position] = self.steps

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
            self.steps += 1
            self.memory_map[self.position] = self.steps
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

            self.position = exploit_pos

        # Wrap up
        self.steps += 1
        self.memory_map[self.position] = self.steps
        self.walk_map[self.position] = self.steps
        print('Arrived at the target position')
        self.wipe_memory_map()
        self.wipe_exploit_map()
        return self.walk_map
