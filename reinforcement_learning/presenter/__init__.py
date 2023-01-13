from typing import Protocol, Callable

from matplotlib import pyplot as plt
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

    def run_exploration(self, explorations: int, start: tuple[int, int], target: tuple[int, int], show_results=False) -> None:
        """Run exploration.

        Args:
            explorations (int): number of explorations
            start (tuple[int, int]): start position
            target (tuple[int, int]): target position

        Returns:
            None
        """
        print('Starting exploration...')
        exploit_map = self.model.explore(self.adjacent_pos, explorations)
        show_map = self.view.map + exploit_map
        distance = self.model.steps
        optimal = self.model.calc_manhattan_distance() + 1
        explorations = self.model.num_explorations
        if show_results:
            metrics = f'Explorations: {explorations}; Steps: {distance}; Optimal: {optimal}; S: {start}; T: {target}'
            self.view.show_map(show_map, 'heatmap', metrics, start, target)

    def run_exploitation(self, start: tuple[int, int], target: tuple[int, int], show_results=False) -> float:
        """Run exploitation.

        Args:
            start (tuple[int, int]): start position
            target (tuple[int, int]): target position

        Returns:
            float: f_rel
        """
        walk_map = self.model.exploit()
        threshhold = walk_map >= 1
        walk_map[threshhold] = 1
        show_map = self.view.map + walk_map
        distance = self.model.steps
        optimal = self.model.calc_manhattan_distance() + 1
        f_rel = abs(distance - optimal) / optimal
        if show_results:
            metrics = f'Distance walked: {distance}; Optimal: {optimal}; F_rel: {f_rel * 100:.2f}%; S: {start}; T: {target}'
            self.view.show_map(show_map, 'heatmap', metrics, start, target)
        return f_rel, show_map

    def run(self, explorations: int = 1, repetitions: int = 1, show_intermediate_results=False) -> None:
        print('Running presenter...')
        self.view.load_map_from_image('reinforcement_learning/view/testmap.png')
        start = self.model.start[::-1]
        target = self.model.target[::-1]

        training_results = []
        best_training_rep = 0
        best_f_rel = 1
        best_map = None
        while len(training_results) < repetitions:
            print(f'\nRepetition: {len(training_results) + 1}')
            self.run_exploration(explorations, start, target, show_intermediate_results)
            f_rel, _map = self.run_exploitation(start, target, show_intermediate_results)
            training_results.append(f_rel)
            print(f'f_rel: {f_rel * 100:.2f}%')
            if f_rel < best_f_rel:
                print(f'New best f_rel: {f_rel * 100:.2f}%')
                best_f_rel = f_rel
                best_map = _map
                best_training_rep = len(training_results)

        print(f'Best f_rel: {best_f_rel * 100:.2f}%')
        average_f_rel = sum(training_results) / len(training_results)
        standard_deviation = np.std(training_results)
        inv_training_results = [1 - f_rel for f_rel in training_results]
        title = f'Best f_rel: {best_f_rel * 100:.2f}% in Rep: {best_training_rep}; S: {start}; T: {target}'
        self.view.show_map(best_map, 'heatmap', title, start, target)

        fig, ax = plt.subplots()
        x_arrange = np.arange(1, len(training_results) + 1)
        rects_bad = ax.bar(x_arrange, training_results, width=0.8, color='orange', label='Bad')
        _ = ax.bar(x_arrange, inv_training_results, width=0.8, color='green', label='Good', bottom=training_results, alpha=0.5)
        ax.axhline(y=average_f_rel, color='red', label='Average')
        if len(training_results) < 20:
            ax.bar_label(rects_bad, fmt='%.2f')
        ax.set_xlim(0, len(training_results) + 1)
        ax.set_ylim(0, 1)
        ax.set_title(f'Training results; Start: {start}; Target: {target}; Avg: {average_f_rel:.2f} +- {standard_deviation:.2f}')
        ax.set_xlabel('Repetition')
        ax.set_ylabel('f_rel')
        ax.legend()
        fig.tight_layout()
        plt.show()
