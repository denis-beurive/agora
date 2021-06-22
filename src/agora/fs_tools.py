"""
This file contains file system utilities.
"""

import os


def create_directory(file_path: str) -> bool:
    """
    Create the directory that would be used to store a file identified by its given path.

    :param file_path: the path to the file.
    :return: if the directory was created, then the function returns the value True.
    Otherwise, it returns the value False.
    """
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False
