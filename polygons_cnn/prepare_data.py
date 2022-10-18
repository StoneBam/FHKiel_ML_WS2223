import os
import shutil

DATA_DIR = os.path.join(os.path.dirname(__file__), ".data/polygons_data")
DATA_CSV = os.path.join(DATA_DIR, "targets.csv")
PICTURES = os.path.join(DATA_DIR, "images/content/images")


def create_subfolders() -> tuple[str, str, str]:
    """Creates subfolders for training, validation and test data.

    Args:
        path (str): base path where directories shall be created in

    Returns:
        tuple[str, str, str]: test_dir, train_dir, validation_dir
    """
    test_dir = os.path.join(DATA_DIR, "test")
    train_dir = os.path.join(DATA_DIR, "train")
    validation_dir = os.path.join(DATA_DIR, "validation")
    try:
        for directory in [test_dir, train_dir, validation_dir]:
            if not os.path.exists(directory):
                os.mkdir(directory)
    except OSError:
        raise
    finally:
        return test_dir, train_dir, validation_dir


def cleanup_subfolders() -> None:
    """Cleans up subfolders of training, validation and test data.

    """
    test_dir = os.path.join(DATA_DIR, "test")
    train_dir = os.path.join(DATA_DIR, "train")
    validation_dir = os.path.join(DATA_DIR, "validation")
    try:
        for directory in [test_dir, train_dir, validation_dir]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
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

    train_len = int(file_list_length * percent_train)
    validate_len = int(file_list_length * percent_train)

    cleanup_subfolders()
    test_dir, train_dir, validation_dir = create_subfolders()

    with open(DATA_CSV, "r") as csvfile:

        for index, line in enumerate(csvfile):
            if index == 0:
                continue
            elif index <= train_len:
                file = line.split(',')[1]
                src = os.path.join(PICTURES, file)
                dst = os.path.join(train_dir, file)
                shutil.copyfile(src, dst)
            elif index <= train_len + validate_len:
                file = line.split(',')[1]
                src = os.path.join(PICTURES, file)
                dst = os.path.join(validation_dir, file)
                shutil.copyfile(src, dst)
            else:
                file = line.split(',')[1]
                src = os.path.join(PICTURES, file)
                dst = os.path.join(test_dir, file)
                shutil.copyfile(src, dst)


if __name__ == "__main__":
    distribute_data()
