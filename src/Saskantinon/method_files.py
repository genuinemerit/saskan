#!python

"""File utilities.

module:    method_files.py
class:     FileMethods/0
author:    GM <genuinemerit @ pm.me>
"""
import json
import pandas as pd
import pickle
import shutil
from method_shell import ShellMethods
from numbers_parser import Document as NumbersDoc
from os import remove, symlink, makedirs
from pathlib import Path
from pprint import pprint as pp  # noqa: F401

SM = ShellMethods()


class FileMethods(object):
    """File IO utilities."""

    def __init__(self):
        """Initialize FileMethods object."""
        pass

    # Read methods
    # ==============================================================

    @classmethod
    def is_file_or_dir(cls, p_path: str) -> bool:
        """
        Check if file or directory exists.

        :param p_path: Legit path to file or dir location.
        :return: True if exists, False otherwise.
        """
        return Path(p_path).exists()

    @classmethod
    def scan_dir(cls, p_dir_path: str, p_file_pattern: str = "") -> list:
        """
        Scan a directory for files matching a specific pattern.
        This method returns PosixPath objects, not strings.

        :param p_dir_path: Path to the directory.
        :param p_file_pattern: Pattern to match the file names. Allow * as wildcard.
        :return: List of file paths (PosixPath structures) matching the pattern.
        """
        srch = p_file_pattern.split("*")
        try:
            dir_path = Path(p_dir_path)
            if dir_path.exists() and dir_path.is_dir():
                files = [
                    f for f in dir_path.iterdir() if all(s in f.name for s in srch)
                ]
                return sorted(files)
        except Exception as err:
            raise err
        return []

    @classmethod
    def get_dir(cls, p_path: str):
        """
        Read a directory and return its contents.

        :param p_path: Legit path to directory location.
        :return: List of directory contents or None if not found.
        """
        try:
            path_obj = Path(p_path)
            if path_obj.exists() and path_obj.is_dir():
                return [str(f) for f in path_obj.iterdir()]
        except Exception as err:
            raise err
        return None

    @classmethod
    def get_absolute_path(cls, p_path: str) -> str:
        """
        Convert provided path to an absolute path.

        :param p_path: Legit path to file or dir location.
        :return: Absolute path as string.
        """
        return str(Path(p_path).resolve())

    @classmethod
    def get_file(cls, p_path: str) -> str:
        """
        Read in an entire file and return its contents.

        :param p_path: Legit path to file location.
        :return: File content as text.
        """
        try:
            abs_path = Path(p_path).resolve()
            with open(abs_path, "r") as f:
                return f.read().strip()
        except Exception as err:
            print(SM.show_trace(err))
        return ""

    @classmethod
    def get_numbers_data(cls, p_file_path: str, p_sheet_x: int = 0) -> pd.DataFrame:
        """
        Read data from Numbers (MacOS) spreadsheet tab and return as a DataFrame.

        :param p_file_path: Path to the workbook.
        :param p_sheet_x: Index of sheet to load.
        :return: DataFrame of the sheet.
        """
        doc = NumbersDoc(p_file_path)
        sheets = doc.sheets
        tables = sheets[p_sheet_x].tables
        data = tables[0].rows(values_only=True)
        return pd.DataFrame(data[1:], columns=data[0])

    def get_spreadsheet_data(self, p_file_path: str, p_sheet: str = "") -> pd.DataFrame:
        """
        Get data from Excel, ODF, CSV (tab), or MacOS Numbers spreadsheet.

        :param p_file_path: Path to the workbook.
        :param p_sheet: Name or index of sheet to load. Optional.
        :return: DataFrame of the sheet.
        """
        ss_type = p_file_path.split(".")[-1].lower()
        sheet_nm = None if not p_sheet else p_sheet
        if ss_type in ("xlsx", "xls"):
            return pd.read_excel(p_file_path, sheet_name=sheet_nm)
        elif ss_type == "ods":
            return pd.read_excel(p_file_path, engine="odf", sheet_name=sheet_nm)
        elif ss_type == "csv":
            return pd.read_csv(p_file_path)
        elif ss_type == "numbers":
            return self.get_numbers_data(p_file_path, int(sheet_nm))
        else:
            raise ValueError(f"Unsupported file type: {p_file_path}")

    @classmethod
    def get_json_file(cls, p_path: str):
        """
        Read in an entire JSON file and return its contents as dict.

        :param p_path: Legit path to JSON file location.
        :return: File content as dictionary or empty dict on error.
        """
        try:
            abs_path = Path(p_path).resolve()
            return json.loads(cls.get_file(abs_path))
        except Exception as e:
            print(SM.show_trace(e))
        return {}

    @classmethod
    def unpickle_object(cls, p_path: str):
        """
        Unpickle an object.

        :param p_path: Legit path to pickled object location.
        :return: Unpickled object.
        """
        try:
            abs_path = Path(p_path).resolve()
            with open(abs_path, "rb") as f:
                return pickle.load(f)
        except Exception as err:
            raise err

    # Write methods
    # ==============================================================
    @classmethod
    def make_dir(cls, p_path: str):
        """
        Create directory at specified location.

        :param p_path: Legit path to create dir.
        """
        try:
            makedirs(p_path, exist_ok=True)
        except Exception as err:
            raise err

    @classmethod
    def delete_file(cls, p_path: str):
        """
        Remove a file.

        :param p_path: Valid path to file to be removed.
        """
        try:
            remove(p_path)
        except OSError as err:
            raise err

    @classmethod
    def copy_one_file(cls, p_path_from: str, p_path_to: str):
        """
        Copy one file from source to target.

        :param p_path_from: Full path of file to be moved.
        :param p_path_to: Destination path.
        """
        try:
            shutil.copy2(p_path_from, p_path_to)
        except OSError as err:
            raise err

    @classmethod
    def copy_all_files(cls, p_path_from: str, p_path_to: str):
        """
        Copy all files in dir from source to target.

        :param p_path_from: Full path of a dir with files to be moved.
        :param p_path_to: Destination path.
        """
        try:
            cmd = f"cp -rf {p_path_from}/* {p_path_to}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise Exception(msg)
        except Exception as err:
            raise err

    @classmethod
    def make_link(cls, p_link_from: str, p_link_to: str):
        """
        Make a symbolic link from the designated file.

        :param p_link_from: Path of file to be linked from.
        :param p_link_to: Destination path of the link.
        """
        try:
            symlink(p_link_from, p_link_to)
        except OSError as err:
            raise err

    @classmethod
    def append_file(cls, p_path: str, p_text: str):
        """
        Append text to specified text file.

        :param p_path: Legit path to a text file location.
        :param p_text: Text to append to the file.
        """
        try:
            with open(p_path, "a+") as f:
                f.write(p_text)
        except Exception as err:
            raise err

    @classmethod
    def write_file(cls, p_path: str, p_data, p_file_type: str = "w+") -> bool:
        """
        Write or overwrite data to specified file.

        :param p_path: Legit path to a file location.
        :param p_data: Data to write to the file.
        :param p_file_type: Mode to open the file, default is "w+".
        :return: True if successful, False otherwise.
        """
        try:
            with open(p_path, p_file_type) as f:
                f.write(p_data)
        except Exception as e:
            raise f"Error writing file: {SM.show_trace(e)}"
            return False
        return True

    @classmethod
    def write_df_to_csv(cls, p_df: pd.DataFrame, p_csv_path: str):
        """
        Save dataframe as CSV.

        :param p_df: Dataframe to save as CSV.
        :param p_csv_path: Path to the CSV file to create.
        """
        p_df.to_csv(p_csv_path, index=False)

    @classmethod
    def pickle_object(cls, p_path: str, p_obj):
        """
        Pickle an object.

        :param p_path: Legit path to target object/file location.
        :param p_obj: Object to be pickled (source).
        """
        try:
            with open(p_path, "wb") as obj_file:
                pickle.dump(p_obj, obj_file)
        except Exception as err:
            raise err

    # CHMOD methods
    # ==============================================================
    @classmethod
    def make_readable(cls, p_path: str):
        """
        Make file at path readable for all.

        :param p_path: File to make readable.
        """
        cls._change_permissions(p_path, "u=rw,g=r,o=r")

    @classmethod
    def make_writable(cls, p_path: str):
        """
        Make file at path writable for all.

        :param p_path: File to make writable.
        """
        cls._change_permissions(p_path, "u=rwx,g=rwx,o=rwx")

    @classmethod
    def make_executable(cls, p_path: str):
        """
        Make file at path executable for all.

        :param p_path: File to make executable.
        """
        cls._change_permissions(p_path, "u=rwx,g=rx,o=rx")

    @classmethod
    def _change_permissions(cls, p_path: str, mode: str):
        """
        Change file permissions using chmod.

        :param p_path: Path to the file whose permissions are to be changed.
        :param mode: Permission mode string.
        """
        try:
            cmd = f"chmod {mode} {p_path}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise Exception(msg)
        except Exception as err:
            raise err

    # Shaping and analysis methods
    # ==============================================================

    @classmethod
    def get_df_col_names(cls, p_df: pd.DataFrame) -> list:
        """
        Get list of column names from a dataframe.

        :param p_df: Dataframe to extract column names from.
        :return: List of column names.
        """
        return list(p_df.columns.values)

    @classmethod
    def get_df_col_unique_vals(cls, p_col: str, p_df: pd.DataFrame) -> list:
        """
        For a dataframe column, return list of unique values.

        :param p_col: Column name to find unique values in.
        :param p_df: Dataframe containing the column.
        :return: Sorted list of unique values in the column.
        """
        u_vals = p_df.dropna(subset=[p_col]).drop_duplicates(subset=[p_col])
        vals = u_vals[p_col].values.tolist()
        return sorted(vals)

    @classmethod
    def get_df_metadata(cls, p_df: pd.DataFrame) -> dict:
        """
        Get metadata from a dataframe.

        :param p_df: Dataframe to extract metadata from.
        :return: Dictionary with row count and unique values per column.
        """
        df_meta = {"row_count": len(p_df.index), "columns": {}}
        cols = cls.get_df_col_names(p_df)
        for col_nm in cols:
            df_meta["columns"][col_nm] = cls.get_df_col_unique_vals(col_nm, p_df)
        return df_meta

    @classmethod
    def diff_files(cls, p_file_a: str, p_file_b: str) -> str:
        """
        Diff two files and return the result.

        :param p_file_a: Path to the first file.
        :param p_file_b: Path to the second file.
        :return: Result of the diff command as a string.
        """
        try:
            cmd = f"diff {p_file_a} {p_file_b}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise Exception(msg)
            return msg
        except Exception as err:
            raise err
