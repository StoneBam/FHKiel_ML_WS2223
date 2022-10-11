import numpy as np


def func_identical(input_param: float) -> float:
    return input_param


def dfunc_identical(_: float) -> float:
    return 1.0


def func_rectified_linear_unit(input_param: float) -> float:
    return input_param if input_param > 0.0 else 0.0


def dfunc_rectified_linear_unit(output_param: float) -> float:
    return 1.0 if output_param > 0.0 else 0.0


def func_sigmoid(input_param: float) -> float:
    return 1 / (1 + np.power(np.e, -input_param))


def dfunc_sigmoid(output_param: float) -> float:
    return output_param * (1 - output_param)
