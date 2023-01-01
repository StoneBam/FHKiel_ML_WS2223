from typing import Protocol, Callable

import numpy as np


class View(Protocol):

    def get_map(self) -> np.ndarray:
        ...

    def set_map(self, _map: np.ndarray) -> None:
        ...

    def show_map(self, _map, _map_key: str) -> None:
        ...

    def show_all_maps(self, _map: np.ndarray) -> None:
        ...


class Model(Protocol):

    def explore(self, adjacent_pos_func: Callable) -> np.ndarray:
        ...

    def exploit(self) -> np.ndarray:
        ...


class Presenter:

    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def adjacent_pos(self, positions: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
        """Get adjacent positions.

        Args:
            positions (list[tuple[int, int]]): possible positions

        Returns:
            dict[str, tuple[int, int]]: adjacent positions
        """
        return {pos: self.view.get_map()[pos] for pos in positions}

    def run(self, explorations: int = 1) -> None:
        exploit_map = self.model.explore(self.adjacent_pos, explorations)
        show_map = self.view.get_map() + exploit_map
        self.view.show_all_maps(show_map)

        walk_map = self.model.exploit()
        show_map = self.view.get_map() + walk_map
        self.view.show_all_maps(show_map)
