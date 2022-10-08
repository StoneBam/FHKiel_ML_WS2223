import random
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


class LinearRegression():

    def __init__(self, data: list, initial_slope: float | None = None, initial_stepw: float | None = None) -> None:
        self._data: list = data

        self._init_slope: float = self.guess_initial_slope() if initial_slope is None else initial_slope
        self._curr_slope: float = self._init_slope
        self._init_stepw: float = self.guess_initial_stepw(self._init_slope) if initial_stepw is None else initial_stepw
        self._curr_stepw: float = self._init_stepw

        self._slope_errors: list = []
        self._last_error: float = float()
        self._curr_error: float = self.calc_current_error(self._curr_slope)

        self._last_frac: float = 0
        self._iterations: int = 0

        self._plot = plt.figure("Linear Regression")

    def guess_initial_slope(self, data: list | None = None) -> float:
        max_y_value: int | float = max(self._data if data is None else data)
        max_x_value: int = len(self._data if data is None else data)
        slope: float = max_y_value / max_x_value
        return slope

    def guess_initial_stepw(self, initial_slope: float, fraction: float = 0.1) -> float:
        if fraction > 1:
            return initial_slope
        elif fraction < 0:
            return 0.0
        else:
            return initial_slope * fraction

    def calc_current_error(self, current_slope: float, data: list | None = None) -> float:
        error: float = 0.0
        y_val: int | float
        for x_val, y_val in enumerate(self._data if data is None else data):
            error += (y_val - x_val * current_slope)**2
        return error

    def calc_next_stepw(self, old_stepw: float, error_diff: float) -> float:
        if error_diff < 0:
            return old_stepw / -2
        else:
            return old_stepw

    def comp_errors(self, last_error: float | None = None, curr_error: float | None = None) -> tuple[float, float]:
        _last_error: float = self._last_error if last_error is None else last_error
        _curr_error: float = self._curr_error if curr_error is None else curr_error
        diff: float = _last_error - _curr_error
        frac: float = _curr_error / _last_error
        return (diff, frac)

    def recursive_approx(self, stepping: int | None = None) -> tuple[float, float, float]:
        # Clear slope-error list on first run
        if self._iterations == 0:
            self._slope_errors.clear()

        # Modify slope with stepwidth
        self._curr_slope += self._curr_stepw

        # Calculate new error
        self._last_error = self._curr_error
        self._curr_error = self.calc_current_error(self._curr_slope)

        # Add slope-error pair to list
        self._slope_errors.append((self._curr_slope, self._curr_error))

        # Get error stats
        diff, frac = self.comp_errors()
        self._curr_stepw = self.calc_next_stepw(self._curr_stepw, diff)
        print(f'Slope: {self._curr_slope}, Stepwidth: {self._curr_stepw},  Error: {self._curr_error}, diff: {diff}, frac: {frac}')

        # Modulo to show only every x steps
        if stepping is not None and stepping > 0:
            if self._iterations % stepping == 0 and self._iterations > 0:
                self.render_diagram(self._curr_slope)
                input(f'Press any key for next iteration ({self._iterations + 1}).')
        self._iterations += 1

        if 1.01 > frac > 0.99 and 1.01 > self._last_frac > 0.99:
            self.render_diagram(self._curr_slope)
            iters: int = self._iterations
            self._iterations = 0
            return (self._curr_slope, self._curr_error, iters)
        else:
            self._last_frac = frac
            return self.recursive_approx(stepping)

    def render_diagram(self, slope: float) -> None:
        self._plot.clf()

        x_value: np.ndarray = np.array(range(len(self._data)))
        y_data: np.ndarray = np.array(self._data)
        y_reg: np.ndarray = np.array([x * slope for x in x_value])
        sub_1 = plt.subplot(121)
        sub_1.plot(x_value, y_data, 'r+', x_value, y_reg, 'g-')
        sub_1.grid(True)
        sub_1.set_title(f'Regression (Iteration = {self._iterations})')
        self._plot.add_subplot(sub_1)

        m_values: np.ndarray = np.array([])
        q_values: np.ndarray = np.array([])
        for m_val, q_val in self._slope_errors:
            m_values = np.append(m_values, m_val)
            q_values = np.append(q_values, q_val)
        perm = m_values.argsort()
        m_values = m_values[perm]
        q_values = q_values[perm]

        sub_2 = plt.subplot(122)
        sub_2.plot(m_values, q_values, 'b.-')
        sub_2.grid(True)
        sub_2.set_title('Q-Error vs. Slope')
        sub_2.set_ylabel('Q-Error')
        sub_2.set_xlabel('Slope')
        sub_2.text(
            0.05,
            0.95,
            f'm = {round(self._curr_slope, 2)}\nF = {round(self._curr_error, 2)}',
            horizontalalignment='left',
            verticalalignment='center',
            transform=sub_2.transAxes)
        self._plot.add_subplot(sub_2)

        self._plot.show()
        return None


class TestLinearRegression:

    data = [x for x in range(100)]
    data_rng = [x + x % 3 for x in range(100)]

    def test_guess_initial_slope(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert round(linreg.guess_initial_slope(), 1) == 1.0

    def test_guess_initial_stepw(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert round(linreg.guess_initial_stepw(1.0), 2) == 0.1

    def test_calc_current_error(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert round(linreg.calc_current_error(1.0), 2) == 0.0

    def test_calc_next_stepw(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.calc_next_stepw(1.0, -1.0) == -0.5

    def test_comp_errors(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.comp_errors(1.0, 0.6) == (0.4, 0.6)

    def test_recursive_approx(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data_rng)
        slope, error, iters = linreg.recursive_approx()
        assert (round(slope, 2), round(error, 2), round(iters, 2)) == (1.02, 91.51, 19)

    def test_render_diagram(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data_rng)
        render = linreg.render_diagram(2.0)
        assert render is None


def generate_random_data(
        seed: str | None = None,
        n_datapoints: int = 100,
        lower_bound: int = 0,
        upper_bound: int = 100,
        function: Callable | None = None,
        noise: int = 0
        ) -> list:

    rng = random.Random(seed)
    if function is not None:
        stepsize = (upper_bound - lower_bound) // n_datapoints
        return [function(x) + (function(x) * 0 + noise * (rng.random() - 0.5)) for x in range(lower_bound, upper_bound, stepsize)]
    else:
        return rng.sample(range(lower_bound, upper_bound), n_datapoints)


def test_generate_random_data() -> None:
    a, b, c, d = generate_random_data('test', 4, -10, 10, lambda x: x)
    assert [round(a, 2), round(b, 2), round(c, 2), round(d, 2)] == [-10.0, -5.0, 0.0, 5.0]


if __name__ == "__main__":
    random_sample = generate_random_data(n_datapoints=250, upper_bound=500, function=lambda x: 1 * x, noise=50)
    linreg = LinearRegression(random_sample)
    linreg.recursive_approx(stepping=1)
    input('Press any key to end program.')