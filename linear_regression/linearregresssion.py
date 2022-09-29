class LinearRegression():

    def __init__(self, data: list, initial_slope: float = None, initial_stepw: float = None) -> None:
        self._data: list = data

        self._init_slope: float = self.guess_initial_slope() if initial_slope is None else initial_slope
        self._curr_slope: float = self._init_slope
        self._init_stepw: float = self.guess_initial_stepw(self._init_slope) if initial_stepw is None else initial_stepw
        self._curr_stepw: float = self._init_stepw

        self._all_errors: dict = {}
        self._last_error: float = None
        self._curr_error: float = 0.0

    def guess_initial_slope(self, data: list = None) -> float:
        max_y_value = max(self._data if data is None else data)
        max_x_value = len(self._data if data is None else data)
        slope: float = max_y_value / max_x_value
        return round(slope, 1)

    def guess_initial_stepw(self, initial_slope: float, fraction: float = 0.01) -> float:
        if fraction > 1:
            return initial_slope
        elif fraction < 0:
            return 0.0
        else:
            return round(initial_slope * fraction, 2)

    def calc_current_error(self, current_slope: float, data: list = None) -> float:
        error = 0.0
        for x_val, y_val in enumerate(self._data if data is None else data):
            error += (y_val - x_val * current_slope)**2
        return error

    def calc_next_stepw(self, old_stepw: float, step_error: float) -> float:
        if step_error < 0:
            return old_stepw / -2
        else:
            return old_stepw / 2

    def comp_errors(self, last_error: float = None, curr_error: float = None) -> tuple[float, float]:
        last_error = self._last_error if last_error is None else last_error
        curr_error = self._curr_error if curr_error is None else curr_error
        diff: float = last_error - curr_error
        frac: float = curr_error / last_error
        return (diff, frac)


class TestLinearRegression:

    data = [x for x in range(100)]
    data_double = [x * 2 for x in range(100)]
    data_half = [x / 2 for x in range(100)]

    def test_guess_initial_slope(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.guess_initial_slope() == 1.0

    def test_guess_initial_stepw(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.guess_initial_stepw(1.0) == 0.01

    def test_calc_current_error(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.calc_current_error(1.0) == 0.0

    def test_calc_next_stepw(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.calc_next_stepw(1.0, -1.0) == -0.5

    def test_comp_errors(self) -> None:
        linreg: LinearRegression = LinearRegression(self.data)
        assert linreg.comp_errors(1.0, 0.6) == (0.4, 0.6)


if __name__ == "__main__":
    pass
