import random
import numpy as np
from typing import Callable

from layer import Layer


class Network:

    def __init__(self, seed: str | None) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.network_shape: list[int] = []
        self.layers: list[Layer]
        self.inputs: np.ndarray
        self.outputs: np.ndarray

    def add_layer(
            self,
            layer_type: str,
            n_neurons: int,
            n_neurons_parent_layer: int,
            transport_func: Callable = lambda x, w: np.dot(x, w),
            activation_func: Callable = lambda x: x,
            pd_activation_func: Callable = lambda x: 1,
            learning_rate: float = 1.0,
            loss_function: Callable = lambda x: sum(x),
            weights: np.ndarray | None = None
            ) -> None:
        self.layers.append(Layer(
            layer_type,
            n_neurons,
            n_neurons_parent_layer,
            transport_func,
            activation_func,
            pd_activation_func,
            learning_rate,
            loss_function,
            weights,
            self.seed))
        self.network_shape.append(n_neurons)

    def train(self, inputs: np.ndarray, outputs: np.ndarray, iterations: int) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.iterations = 0
        self.outputs_actual: np.ndarray

        def forward_pass(_inputs: np.ndarray):
            _outputs: np.ndarray = np.array([])
            layer: Layer
            for index, layer in enumerate(self.layers):
                if index == 0:
                    _outputs = layer.forward_pass(_inputs)
                if index == len(self.layers):
                    self.outputs_actual = layer.forward_pass(_outputs)
                else:
                    _outputs = layer.forward_pass(_outputs)

        def backward_pass(_output: float):
            _inputs: np.ndarray = np.array([])
            layer: Layer
            for index in range(len(self.layers)):
                i_reversed = -index - 1
                layer = self.layers[i_reversed]
                if index == 0:
                    _total_error = self.layers[index].calc_loss()
                    layer.weights = layer.backward_pass(_total_error, _output)
                if index == len(self.layers):
                    pass
                else:
                    pass

        sample = self.rng.choice(range(len(self.inputs)))
        forward_pass(self.inputs[sample])
        for iteration in range(self.iterations):
            for _ in range(len(self.inputs)):
                sample = self.rng.choice(range(len(self.inputs)))
                backward_pass(self.outputs[sample])
                forward_pass(self.inputs[sample])
