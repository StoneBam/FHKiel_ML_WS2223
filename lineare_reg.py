

class linear_reg():

    def __init__(self, start_step_width: float, initial_slope: float, values: list) -> None:
        self._step_width: float = start_step_width
        self._slope: float = initial_slope

        self._value_array: list[float] = values
        self._value_slope: float = 0.0

    def find_slope(self):
        error: float = 0.0
        while error/self._value_slope: # TODO
            for index, value in enumerate(self._value_array):
                pass

    def calc_error_square(self, x_value, yvalue) -> float:
        return (x_value - yvalue)**2


if __name__ == "__main__":
    pass
