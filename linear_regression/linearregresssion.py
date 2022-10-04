class LinearRegression():

    def __init__(self, data: list, initial_slope: float = None, initial_stepw: float = None) -> None:
        self._data: list = data

        self._init_slope: float = self.guess_initial_slope() if initial_slope is None else initial_slope
        self._curr_slope: float = self._init_slope
        self._init_stepw: float = self.guess_initial_stepw(self._init_slope) if initial_stepw is None else initial_stepw
        self._curr_stepw: float = self._init_stepw

        self._last_error: float = None
        self._curr_error: float = self.calc_current_error(self._curr_slope)

        self._iterations: int = 0

    def guess_initial_slope(self, data: list = None) -> float:
        max_y_value = max(self._data if data is None else data)
        max_x_value = len(self._data if data is None else data)
        slope: float = max_y_value / max_x_value
        return slope

    def guess_initial_stepw(self, initial_slope: float, fraction: float = 0.01) -> float:
        if fraction > 1:
            return initial_slope
        elif fraction < 0:
            return 0.0
        else:
            return initial_slope * fraction

    def calc_current_error(self, current_slope: float, data: list = None) -> float:
        error = 0.0
        for x_val, y_val in enumerate(self._data if data is None else data):
            error += (y_val - x_val * current_slope)**2
        return error

    def calc_next_stepw(self, old_stepw: float, error_diff: float) -> float:
        if error_diff < 0:
            return old_stepw / -2
        else:
            return old_stepw

    def comp_errors(self, last_error: float = None, curr_error: float = None) -> tuple[float, float]:
        last_error = self._last_error if last_error is None else last_error
        curr_error = self._curr_error if curr_error is None else curr_error
        diff: float = last_error - curr_error
        frac: float = curr_error / last_error
        return (diff, frac)

    def recursive_approx(self, stepping: int = None) -> tuple[float, float, float]:
        if stepping is not None:
            if self._iterations % stepping == 0:
                input('Press any key for next iteration.')
        self._iterations += 1

        # Modify slope with stepwidth
        self._curr_slope += self._curr_stepw

        # Calculate new error
        self._last_error = self._curr_error
        self._curr_error = self.calc_current_error(self._curr_slope)

        # Get error stats
        diff, frac = self.comp_errors()
        self._curr_stepw = self.calc_next_stepw(self._curr_stepw, diff)

        if 1.01 > frac > 0.99:
            iters = self._iterations
            self._iterations = 0
            return (self._curr_slope, self._curr_error, iters)
        else:
            return self.recursive_approx(stepping)


class TestLinearRegression:

    data = [x for x in range(100)]
    data_rng = [x + x % 3 for x in range(100)]

    def test_guess_initial_slope(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert round(linreg.guess_initial_slope(), 1) == 1.0

    def test_guess_initial_stepw(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert round(linreg.guess_initial_stepw(1.0), 2) == 0.01

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
        assert (round(slope, 2), round(error, 2), round(iters, 2)) == (1.02, 99.66, 2)


if __name__ == "__main__":
    pass
