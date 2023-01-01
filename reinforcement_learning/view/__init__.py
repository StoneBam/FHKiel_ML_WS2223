import argparse
from typing import Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from PIL import Image
from scipy import ndimage


class Environment:

    def __init__(self, mapsize: tuple[int, int] = (10, 10)) -> None:
        self.mapsize = (x + 2 for x in mapsize)

        self.info_layers: dict[str, Callable] = {
            'heatmap': self.heatmap,
            'contourmap': self.contourmap
        }

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
        return image

    def save_map_to_image(self, _map: np.ndarray, image_path: str) -> None:
        """Save a map to an image.

        Args:
            _map (np.ndarray): map to be saved
            image_path (str): path to the image

        Returns:
            None
        """
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
        sns.heatmap(_map, annot=annot, fmt=".2f", cmap="RdYlGn", ax=ax, cbar=cbar, square=True, vmin=-1, vmax=1)

    # Map display methods

    def show_map(self, _map, _map_key: str) -> None:
        """Show a single map with a specific visualization method.

        Args:
            _map (np.ndarray): map to be displayed
            _map_key (str): key of the visualization method to be used

        Returns:
            None
        """
        _, ax = plt.subplots(1, 1, figsize=(5, 5), subplot_kw={'aspect': 'equal'})
        self.info_layers.get(_map_key, self.heatmap)(_map, ax)
        plt.tight_layout()
        plt.show()

    def show_all_maps(self, _map: np.ndarray) -> None:
        """Show all maps with all visualization methods.

        Args:
            _map (np.ndarray): map to be displayed

        Returns:
            None
        """
        _, axes = plt.subplots(1, 2, figsize=(10, 5), subplot_kw={'aspect': 'equal'})
        self.heatmap(_map, axes[0], False)
        self.contourmap(_map, axes[1])
        plt.tight_layout()
        plt.show()


def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mapsize', type=int, nargs=2, default=(10, 10))
    parser.add_argument('-d', '--display', type=str, default='heatmap')
    parser.add_argument('-l', '--load', type=str, default='testmap.png')
    parser.add_argument('-s', '--save', type=str, default=None)
    parser.add_argument('-b', '--no-borders', action='store_false', dest='borders')
    args = parser.parse_args()

    # Create environment
    env = Environment(args.mapsize)

    # Random maps
    rng_map = env.create_random_map()
    env.show_map(rng_map, args.display)
    env.show_all_maps(rng_map)

    # Maps from images
    if args.load:
        img_map = env.load_map_from_image(args.load, borders=args.borders)
        env.show_map(img_map, args.display)


if __name__ == "__main__":
    main()
