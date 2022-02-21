#!python3.9

"""File IO utilities.

module:    file_io.py
class:     FileIO/0
author:    GM <genuinemerit @ pm.me>
"""
# from os import path
from os import system
from pathlib import Path


class FileIO(object):
    """File IO utilities."""

    def __init__(self):
        """Initialize FileIO object."""
        pass

    def make_dir(self,
                 p_path: str) -> tuple:
        """Create directory at specified location.

        Success if directory already exists.

        Args:
            p_path (str): Legit path to create dir.
        Return:
            (tuple): (Status (bool), Message (str or None))
        """

        if not Path(p_path).exists():
            system(f"mkdir {p_path}")
        if Path(p_path).exists():
            return (True, None)
        else:
            return (False, "Directory creation failed.")

    def append_file(self,
                    p_path: str,
                    p_text: str) -> tuple:
        """Append text to specified file.

        Create file if it does not already exist.

        Args:
            p_path (str): Legit path to a file location.
            p_text (str): Text to append to the file.
        Return:
            (tuple): (Status (bool), Message (str or None))
        """

        try:
            f = open(p_path, 'a+')
            f.write(p_text)
            f.close()
        except Exception as err:
            return (False, err)
        return (True, None)

    def write_file(self,
                   p_path: str,
                   p_text: str) -> tuple:
        """Write or overwrite text to specified file.

        Create file if it does not already exist.
        Overwrite file if it does already exist.

        Args:
            p_path (str): Legit path to a file location.
            p_text (str): Text to append to the file.
        Return:
            (tuple): (Status (bool), Message (str or None))
        """

        try:
            f = open(p_path, 'w+')
            f.write(p_text)
            f.close()
        except Exception as err:
            return (False, err)
        return (True, None)

    def get_file(self,
                 p_path: str) -> tuple:
        """Read in an entire file and return ites contents.

        Args:
            p_path (str): Legit path to file location.
        Return
            (Tuple): (Status (bool), Message (text or None),
                      File content (Text, Bytes or None))
        """
        content = None
        try:
            if Path(p_path).exists():
                with open(p_path, "r") as f:
                    content = f.read().strip()
                f.close()
                return (True, None, content)
            else:
                return (False, None, None)
        except Exception as err:
            return (False, err, None)
