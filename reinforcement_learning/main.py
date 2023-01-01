import argparse

from model import Roboid
from presenter import Presenter
from view import Environment


def sanity_check_args(args: argparse.Namespace) -> None:
    """Sanity check the arguments.

    Args:
        args (argparse.Namespace): arguments

    Raises:
        ValueError: if the arguments are invalid
    """
    # Check the map size
    if args.mapsize[0] <= 0 or args.mapsize[1] <= 0:
        raise ValueError("Map size must be greater than 0")

    # Check the start position
    if args.start[0] < 0 or args.start[1] < 0:
        raise ValueError("Start position must be greater than 0")
    if args.start[0] >= args.mapsize[0] or args.start[1] >= args.mapsize[1]:
        raise ValueError("Start position must be inside the map")

    # Check the target position
    if args.target[0] < 0 or args.target[1] < 0:
        raise ValueError("Target position must be greater than 0")
    if args.target[0] >= args.mapsize[0] or args.target[1] >= args.mapsize[1]:
        raise ValueError("Target position must be inside the map")

    # Check the number of explorations
    if args.explorations <= 0:
        raise ValueError("Number of explorations must be greater than 0")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mapsize', type=int, nargs=2, default=(20, 20))
    parser.add_argument('-s', '--start', type=int, nargs=2, default=(18, 18))
    parser.add_argument('-t', '--target', type=int, nargs=2, default=(2, 2))
    parser.add_argument('-e', '--explorations', type=int, default=20)
    args = parser.parse_args()

    # Sanity check the arguments
    sanity_check_args(args)

    # Arguments
    mapshape = args.mapsize
    pos_start = args.start
    pos_target = args.target

    # Create model, view and presenter
    model = Roboid(mapshape, pos_start, pos_target)
    view = Environment(mapshape)
    presenter = Presenter(model, view)

    # Run the application
    presenter.run(args.explorations)


if __name__ == "__main__":
    main()
