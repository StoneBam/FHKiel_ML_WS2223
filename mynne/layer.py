from typing import Callable
import random
import numpy as np
from neuron import Neuron


class Layer:

    def __init__(
            self,
            layer_type: str,
            n_neurons: int,
            n_neurons_parent_layer: int,
            transport_func: Callable = lambda x, w: np.dot(x, w),
            activation_func: Callable = lambda x: x,
            pd_activation_func: Callable = lambda x: 1,
            learning_rate: float = 1.0,
            loss_function: Callable = lambda x: sum(x),
            weights: np.ndarray | None = None,
            seed: str | None = None
            ) -> None:
        self.layer_type: str = self.set_type(layer_type)
        self.n_neurons: int = n_neurons
        self.loss_function: Callable = loss_function

        # Create Neurons with weights
        self.neurons = [Neuron(transport_func, activation_func, pd_activation_func, learning_rate) for _ in range(n_neurons)]
        self.initialize_weights(n_neurons_parent_layer, weights, seed)

        self.outputs: np.ndarray = np.array([])
        self.weights: np.ndarray = np.array([])

    def set_type(self, layer_type: str) -> str:
        if isinstance(layer_type, str):
            lt = layer_type.lower()
            if lt == 'input':
                return 'input'
            elif lt == 'hidden':
                return 'hidden'
            elif lt == 'output':
                return 'output'
            else:
                raise ValueError(f'"{lt}" is not a valid value for layer_type!')

    def initialize_weights(self, n_neurons_parent_layer: int, weights: np.ndarray | None, seed: str | None,) -> None:
        if weights is None:
            for neuron in self.neurons:
                neuron.set_weights(np.array([random.Random(seed).random() for _ in range(n_neurons_parent_layer)]))
        else:
            for neuron in self.neurons:
                neuron.set_weights(weights)

    def calc_loss(self) -> float:
        return self.loss_function([err.total_error for err in self.neurons])

    def forward_pass(self, inputs: np.ndarray) -> np.ndarray:
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.forward_pass(inputs, self.weights))
        self.outputs = np.array(outputs)
        return self.outputs

    def backward_pass(self, total_error: float, output: float) -> np.ndarray:
        weights = []
        for neuron in self.neurons:
            weights.append(neuron.backward_pass(total_error, output))
        self.weights = np.array(weights)
        return self.weights
