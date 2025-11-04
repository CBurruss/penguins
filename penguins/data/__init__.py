import os

DATA_DIR = os.path.dirname(__file__)

def get_data_path(filename):
    """Get the full path to a data file."""
    return os.path.join(DATA_DIR, filename)