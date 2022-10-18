import os
import shutil

DATA_DIR = os.path.join(os.path.dirname(__file__), ".data/polygons_data")
SORT_DIR = os.path.join(DATA_DIR, "sorted_polygons")
DATA_CSV = os.path.join(DATA_DIR, "targets.csv")
PICTURES = os.path.join(DATA_DIR, "images/content/images")


def create_subfolders() -> tuple[str, str, str, str]:
    """Creates subfolders different shapes.

    Args:
        path (str): base path where directories shall be created in

    Returns:
        tuple[str, str, str, str]: trigon_dir, tetragon_dir, pentagon_dir, hexagon_dir
    """
    dirs = (
        os.path.join(SORT_DIR, "trigon"),
        os.path.join(SORT_DIR, "tetragon"),
        os.path.join(SORT_DIR, "pentagon"),
        os.path.join(SORT_DIR, "hexagon")
    )
    try:
        for directory in dirs:
            if not os.path.exists(SORT_DIR):
                print(f'Create dir {SORT_DIR}')
                os.mkdir(SORT_DIR)
            if not os.path.exists(directory):
                print(f'Create dir {directory}')
                os.mkdir(directory)
    except OSError:
        raise
    finally:
        return dirs


def cleanup_subfolders() -> None:
    """Cleans up subfolders of shapes.
    """
    try:
        if os.path.exists(SORT_DIR):
            print(f'Deleting dir {SORT_DIR}')
            shutil.rmtree(SORT_DIR)
    except Exception:
        raise


def distribute_data(percent_train: float = 0.8, percent_validate: float = 0.1, percent_test: float = 0.1) -> None:
    """Distributes files from data directory to subdirectories

    Args:
        percent_train (float, optional): Defaults to 0.8.
        percent_validate (float, optional): Defaults to 0.1.
        percent_test (float, optional): Defaults to 0.1.

    Raises:
        ValueError: Added percantages can't be bigger than 1!
    """
    if (percent_train + percent_validate + percent_test) > 1:
        raise ValueError("Added percantages can't be bigger than 1!")

    file_list_length = len([f for f in os.listdir(PICTURES) if os.path.isfile(os.path.join(PICTURES, f))])

    cleanup_subfolders()
    trigon_dir, tetragon_dir, pentagon_dir, hexagon_dir = create_subfolders()

    with open(DATA_CSV, "r") as csvfile:
        for index, line in enumerate(csvfile):
            if index == 0:
                continue
            spline = line.split(',')
            file = spline[1]
            sides = int(spline[2])
            if sides == 3:
                src = os.path.join(PICTURES, file)
                dst = os.path.join(trigon_dir, file)
                print(f"\033[91m{index}/{file_list_length}\033[0m - Copy file...", end='\r')
                shutil.copyfile(src, dst)
            elif sides == 4:
                src = os.path.join(PICTURES, file)
                dst = os.path.join(tetragon_dir, file)
                print(f"\033[91m{index}/{file_list_length}\033[0m - Copy file...", end='\r')
                shutil.copyfile(src, dst)
            elif sides == 5:
                src = os.path.join(PICTURES, file)
                dst = os.path.join(pentagon_dir, file)
                print(f"\033[91m{index}/{file_list_length}\033[0m - Copy file...", end='\r')
                shutil.copyfile(src, dst)
            elif sides == 6:
                src = os.path.join(PICTURES, file)
                dst = os.path.join(hexagon_dir, file)
                print(f"\033[91m{index}/{file_list_length}\033[0m - Copy file...", end='\r')
                shutil.copyfile(src, dst)
        print(f"\033[92m{file_list_length}/{file_list_length}\033[0m - Copy file...", end='\r')
    print('\nFile distribution done.')


if __name__ == "__main__":
    distribute_data()
