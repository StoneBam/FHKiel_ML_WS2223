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
    if args.start is not None:
        if args.start[0] < 0 or args.start[1] < 0:
            raise ValueError("Start position must be greater than 0")
        if args.start[0] >= args.mapsize[0] or args.start[1] >= args.mapsize[1]:
            raise ValueError("Start position must be inside the map")

    # Check the target position
    if args.target is not None:
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
    parser.add_argument('-s', '--start', type=int, nargs=2)
    parser.add_argument('-t', '--target', type=int, nargs=2)
    parser.add_argument('-e', '--explorations', type=int, default=20)
    parser.add_argument('-r', '--repeat', type=int, default=1)
    parser.add_argument('-i', '--intermediate', action='store_true', default=False)
    args = parser.parse_args()

    # Sanity check the arguments
    sanity_check_args(args)

    # Arguments
    mapshape = tuple(args.mapsize)
    pos_start = tuple(args.start) if args.start is not None else None
    pos_target = tuple(args.target) if args.target is not None else None

    # Create model, view and presenter
    model = Roboid(mapshape, pos_start, pos_target)
    view = Environment(mapshape)
    presenter = Presenter(model, view)

    # Run the application
    presenter.run(args.explorations, args.repeat, args.intermediate)


if __name__ == "__main__":
    main()
