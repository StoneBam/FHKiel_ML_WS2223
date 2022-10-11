from typing import Callable
import numpy as np


class Neuron:

    def __init__(
            self,
            transport_func: Callable = lambda x, w: np.dot(x, w),
            activation_func: Callable = lambda x: x,
            pd_activation_func: Callable = lambda x: 1,
            learning_rate: float = 1.0
            ) -> None:

        # Inputs
        self.inputs: np.ndarray

        # Weights
        self.weights: np.ndarray

        # Net input
        self.func_net: Callable = transport_func
        self.net: float

        # Activation
        self.func_act: Callable = activation_func

        # Output
        self.output_actual: float

        # Errors
        self.squared_error: float

        # Backpropagation
        self.learning_rate: float = learning_rate
        self.total_error: float
        self.output_ideal: float
        self.pd_error_out: float
        self.func_pd_out_net: Callable = pd_activation_func
        self.pd_out_net: float
        self.pd_net_weights: np.ndarray
        self.weight_deltas: np.ndarray

    def calc_net(self) -> float:
        return self.func_net(self.weights, self.inputs)

    def activate(self) -> float:
        return self.func_act(self.net)

    def calc_squared_error(self) -> float:
        return 0.5 * np.square(self.output_ideal - self.output_actual)

    def set_weights(self, weights: np.ndarray) -> None:
        self.weights: np.ndarray = weights

    def forward_pass(self, inputs: np.ndarray, weights: np.ndarray) -> float:
        self.inputs: np.ndarray = inputs
        self.weights: np.ndarray = weights
        self.net: float = self.calc_net()
        self.output_actual: float = self.activate()
        self.squared_error: float = self.calc_squared_error()
        return self.output_actual

    def backward_pass(self, total_error: float, output_ideal: float) -> np.ndarray:

        # Total error and ideal output from upper layer
        self.total_error = total_error
        self.output_ideal = output_ideal

        # Partial derivatives for backpropagation
        self.pd_error_out = -(self.output_ideal - self.output_actual)
        self.pd_out_net = self.func_pd_out_net(output_ideal)
        self.pd_net_weights = self.inputs
        self.weight_deltas = self.pd_error_out * self.pd_out_net * self.pd_net_weights

        # New weights for next forward pass
        self.weights -= self.learning_rate * self.weight_deltas
        return self.weights
