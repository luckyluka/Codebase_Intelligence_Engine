import os


def scan_directory(root_path):
    """
    Recursively scans a directory and returns a list of file paths.

    Args:
        root_path (str): Root directory to scan

    Returns:
        List[str]: List of file paths
    """
    file_paths = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_paths.append(full_path)

    return file_paths