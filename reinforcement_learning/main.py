from model import Roboid
from presenter import Presenter
from view import Environment


def main():
    # Create model, view and presenter
    model = Roboid()
    view = Environment()
    presenter = Presenter(model, view)

    # Run the application
    presenter.run()


if __name__ == "__main__":
    main()
