import argparse
from typing import Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
from scipy import ndimage


class Environment:

    def __init__(self, mapsize: tuple[int, int] = (10, 10)) -> None:
        self._info_layers: dict[str, Callable] = {
            'heatmap': self.heatmap,
            'contourmap': self.contourmap
        }
        self.mapsize = mapsize
        self.map = self.create_empty_map(borders=True)

    @property
    def mapsize(self) -> tuple[int, int]:
        """Get the map size.

        Returns:
            tuple[int, int]: map size
        """
        return self._mapsize

    @mapsize.setter
    def mapsize(self, _mapsize: tuple[int, int]) -> None:
        """Set the map size.

        Args:
            _mapsize (tuple[int, int]): map size to be set

        Returns:
            None
        """
        if _mapsize[0] < 0 and _mapsize[1] < 0:
            raise ValueError('Map size must be positive.')
        if _mapsize[0] < 4 or _mapsize[1] < 4:
            raise ValueError('Map size must be at least 4x4.')
        self._mapsize = _mapsize

    @property
    def map(self) -> np.ndarray:
        """Get the map.

        Returns:
            np.ndarray: map
        """
        return self._map

    @map.setter
    def map(self, _map: np.ndarray) -> None:
        """Set the map.

        Args:
            _map (np.ndarray): map to be set

        Returns:
            None
        """
        if _map.shape != self.mapsize:
            raise ValueError('Map size does not match.')
        self._map = _map

    @property
    def info_layers(self) -> dict[str, Callable]:
        """Get the info layers.

        Returns:
            dict[str, Callable]: info layers
        """
        return self._info_layers

    # Map creation methods

    def create_empty_map(self, borders: bool = False) -> np.ndarray:
        """Create an empty map with all values set to 0.

        Args:
            borders (bool, optional): Place borders. Defaults to False.

        Returns:
            np.ndarray: empty map
        """
        _map = np.zeros(self.mapsize, dtype=np.float64)
        if borders:
            _map = self.place_borders(_map)
        return _map

    def create_random_map(self, borders: bool = True) -> np.ndarray:
        """Create a random map with values between 0 and 1.

        Args:
            borders (bool, optional): Place borders. Defaults to True.

        Returns:
            np.ndarray: random map
        """
        _map = np.random.rand(*self.mapsize)
        if borders:
            _map = self.place_borders(_map)
        return _map

    def place_borders(self, _map: np.ndarray) -> np.ndarray:
        """Place borders around the map. A border is a negative value.

        Args:
            _map (np.ndarray): map to be modified

        Returns:
            np.ndarray: map with borders
        """
        _map[0, :] = -1
        _map[-1, :] = -1
        _map[:, 0] = -1
        _map[:, -1] = -1
        return _map

    def load_map_from_image(self, image_path: str, borders: bool = True) -> np.ndarray:
        """Load a map from an image.

        Args:
            image_path (str): path to the image
            borders (bool, optional): Place borders. Defaults to True.

        Returns:
            np.ndarray: map loaded from the image
        """
        image = Image.open(image_path)
        self.mapsize = image.size
        image = np.array(image, dtype=np.float64)
        image = image[:, :, 0] / 255 if image.ndim == 3 else image / 255
        threshold = 0 >= image
        image[threshold] = -1
        if borders:
            image = self.place_borders(image)
        self.map = image
        return image

    def save_map_to_image(self, image_path: str) -> None:
        """Save a map to an image.

        Args:
            image_path (str): path to the image

        Returns:
            None
        """
        _map = self.map.copy()
        threshold = 0 > _map
        _map[threshold] = 0
        image = Image.fromarray(np.uint8(_map * 255))
        image.save(image_path, bitmap_format="PNG")

    # Map visualization methods

    def contourmap(self, _map: np.ndarray, ax: plt.Axes) -> None:
        """Visualize a map as a contour map.

        Args:
            _map (np.ndarray): map to be visualized
            ax (plt.Axes): Axes object to be used for visualization

        Returns:
            None
        """
        blurred_map = ndimage.gaussian_filter(_map, sigma=0.5)
        map_axis = [np.array(range(size)) for size in self.mapsize]
        loc = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        contour_source = ax.contour(*map_axis[::-1], blurred_map, antialiased=True, vmin=0, vmax=1, extend="both", levels=loc)
        ax.clabel(contour_source, inline=True, fontsize=8, fmt="%.1f")
        ax.xaxis.tick_top()
        ax.grid(True, which='both', color='g', linewidth=0.5)
        ax.invert_yaxis()

    def heatmap(self, _map: np.ndarray, ax: plt.Axes, cbar: bool = True) -> None:
        """Visualize a map as a heatmap.

        Args:
            _map (np.ndarray): map to be visualized
            ax (plt.Axes): Axes object to be used for visualization
            cbar (bool, optional): Show colorbar. Defaults to True.
        """
        ax.xaxis.tick_top()
        annot = True if max(_map.shape) <= 20 else False
        fmt = ".2f" if max(_map.shape) <= 20 else ".1f"
        sns.heatmap(_map, annot=annot, fmt=fmt, cmap="RdYlGn", ax=ax, cbar=cbar, square=True, vmin=-1)

    # Map display methods

    def maximize_window(self) -> None:
        """Maximize the window depending on the backend.

        Returns:
            None
        """
        mng = plt.get_current_fig_manager()
        match plt.get_backend():
            case "TkAgg":
                mng.window.state("zoomed")
            case "Qt4Agg":
                mng.window.showMaximized()
            case "Qt5Agg":
                mng.window.showMaximized()
            case "MacOSX":
                mng.window.showMaximized()
            case "WXAgg":
                mng.frame.Maximize(True)
            case "GTKAgg":
                mng.window.maximize()
            case "GTK3Agg":
                mng.window.maximize()
            case _:
                pass

    def show_map(
            self,
            _map: np.ndarray,
            _map_key: str,
            title: str = '',
            start: tuple[int, int] = None,
            target: tuple[int, int] = None
            ) -> None:
        """Show a single map with a specific visualization method.

        Args:
            _map (np.ndarray): map to be displayed
            _map_key (str): key of the visualization method to be used

        Returns:
            None
        """
        _, ax = plt.subplots(1, 1, subplot_kw={'aspect': 'equal'})
        self.info_layers.get(_map_key, self.heatmap)(_map, ax)
        if start is not None:
            start = tuple((x + 0.5 for x in start))
            ax.add_patch(Circle(start, 0.5, color='b', fill=False, clip_on=False))
        if target is not None:
            target = tuple((x + 0.5 for x in target))
            ax.add_patch(Circle(target, 0.5, color='k', fill=False, clip_on=False))
        plt.title(title)
        plt.tight_layout()
        self.maximize_window()
        plt.show()

    def show_all_maps(
            self,
            _map: np.ndarray,
            title: str = '',
            start: tuple[int, int] = None,
            target: tuple[int, int] = None
            ) -> None:
        """Show all maps with all visualization methods.

        Args:
            _map (np.ndarray): map to be displayed

        Returns:
            None
        """
        _, axes = plt.subplots(1, 2, subplot_kw={'aspect': 'equal'})
        self.heatmap(_map, axes[0], False, start, target)
        self.contourmap(_map, axes[1])
        plt.title(title)
        plt.tight_layout()
        self.maximize_window()
        plt.show()


def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mapsize', type=int, nargs=2, default=(10, 10), help='Map size (width, height)')
    parser.add_argument('-d', '--display', type=str, default='heatmap', help='Map display method')
    parser.add_argument('-l', '--load', type=str, help='Load map from image')
    parser.add_argument('-r', '--random', action='store_true', help='Create random map')
    parser.add_argument('-s', '--save', type=str, default=None, help='Save map to image')
    parser.add_argument('-b', '--no-borders', action='store_false', dest='borders', help='Remove borders from map')
    args = parser.parse_args()

    # Create environment
    env = Environment(args.mapsize)

    if args.random:
        rng_map = env.create_random_map(args.borders)
        env.show_map(rng_map, args.display, "Random map")
        env.show_all_maps(rng_map)
    elif args.load:
        img_map = env.load_map_from_image(args.load, borders=args.borders)
        env.show_map(img_map, args.display, "Image map")
    else:
        empty_map = env.create_empty_map(args.borders)
        env.show_map(empty_map, args.display, "Empty map")

    # Save maps to images
    if args.save:
        env.save_map_to_image(args.save)


if __name__ == "__main__":
    main()
