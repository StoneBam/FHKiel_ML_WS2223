from typing import Protocol


class View(Protocol):
    ...


class Model(Protocol):
    ...


class Presenter:

    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def run(self) -> None:
        raise NotImplementedError
