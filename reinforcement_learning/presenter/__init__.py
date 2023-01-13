from typing import Protocol, Callable

import numpy as np


class View(Protocol):

    @property
    def mapsize(self) -> tuple[int, int]:
        ...

    @mapsize.setter
    def mapsize(self, _mapsize: tuple[int, int]) -> None:
        ...

    @property
    def map(self) -> np.ndarray:
        ...

    @map.setter
    def map(self, _map: np.ndarray) -> None:
        ...

    def show_map(self, _map, _map_key: str, title: str) -> None:
        ...

    def show_all_maps(self, _map: np.ndarray, title: str) -> None:
        ...

    def load_map_from_image(self, image_path: str, borders: bool = True) -> np.ndarray:
        ...


class Model(Protocol):

    def explore(self, adjacent_pos_func: Callable) -> np.ndarray:
        ...

    def exploit(self) -> np.ndarray:
        ...

    def calc_manhattan_distance(self) -> int:
        ...

    @property
    def steps(self) -> int:
        ...

    @property
    def num_explorations(self) -> int:
        ...

    @property
    def start(self) -> tuple[int, int]:
        ...

    @property
    def target(self) -> tuple[int, int]:
        ...

    def check_start_and_target(self, pos_check: Callable[[tuple[int, int]], float]) -> None:
        ...


class Presenter:

    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

        self.model.check_start_and_target(self.pos_value)

    def adjacent_pos(self, positions: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
        """Get adjacent positions.

        Args:
            positions (list[tuple[int, int]]): possible positions

        Returns:
            dict[str, tuple[int, int]]: adjacent positions
        """
        return {pos: self.view.map[pos] for pos in positions}

    def pos_value(self, pos: tuple[int, int]) -> int:
        """Get the value of the current position.

        Args:
            pos (tuple[int, int]): current position

        Returns:
            int: value of the current position
        """
        return self.view.map[pos]

    def run(self, explorations: int = 1) -> None:
        print('Running presenter...')
        self.view.load_map_from_image('reinforcement_learning/view/testmap.png')
        start = self.model.start[::-1]
        target = self.model.target[::-1]

        print('Starting exploration...')
        exploit_map = self.model.explore(self.adjacent_pos, explorations)
        show_map = self.view.map + exploit_map
        distance = self.model.steps
        optimal = self.model.calc_manhattan_distance() + 1
        explorations = self.model.num_explorations
        metrics = f'Explorations: {explorations}; Steps: {distance}; Optimal: {optimal}; S: {start}; T: {target}'
        self.view.show_map(show_map, 'heatmap', metrics, start, target)

        walk_map = self.model.exploit()
        threshhold = walk_map >= 1
        walk_map[threshhold] = 1
        show_map = self.view.map + walk_map
        distance = self.model.steps
        optimal = self.model.calc_manhattan_distance() + 1
        f_rel = abs(distance - optimal) / optimal
        metrics = f'Distance walked: {distance}; Optimal: {optimal}; F_rel: {f_rel * 100:.2f}%; S: {start}; T: {target}'
        self.view.show_map(show_map, 'heatmap', metrics, start, target)
