import os

def create_file(file_path: str) -> None:
    """
    Create a file and its parent directories if they don't exist.

    Parameters:
    - file_path (str): Absolute path to the file.

    Returns:
    - None
    """
    # Ensure the directory structure exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass