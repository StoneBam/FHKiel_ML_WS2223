from model import Model
from presenter import Presenter
from view import View


def main():
    # Create model, view and presenter
    model = Model()
    view = View()
    presenter = Presenter(model, view)

    # Run the application
    presenter.run()


if __name__ == "__main__":
    main()
