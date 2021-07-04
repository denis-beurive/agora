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


def create_file(file_path: str, override_flag: bool) -> bool:
    """
    Test whether a file should be created or not.

    :param file_path: path to the file.
    :param override_flag: flag that indicates whether an existing file should be overrode or not.
    :return: if the file should be created, then the function returns the value True.
    Otherwise, it returns the value False.
    """
    return (not os.path.exists(file_path)) or override_flag
