#!python

"""File utilities.

module:    method_files.py
class:     FileMethods/0
author:    GM <genuinemerit @ pm.me>
"""
import json

# trunk-ignore(bandit/B403)
import pickle
import shutil
from os import remove, symlink, system
from pathlib import Path
from pprint import pprint as pp  # noqa: F401

import pandas as pd
from method_shell import ShellMethods
from numbers_parser import Document as NumbersDoc

SM = ShellMethods()


class FileMethods(object):
    """File IO utilities."""

    def __init__(self):
        """Initialize FileIO object."""
        pass

    # Read methods
    # ==============================================================

    @classmethod
    def scan_dir(cls, p_dir_path: str, p_file_pattern: str = "") -> list:
        """Scan a directory for files matching a specific pattern.

        Args:
            p_dir_path (str): Path to the directory.
            p_file_pattern (str): Pattern to match the file names.
                Not regex. Allow for * as wildcard, that's it.
                Optional. If not provided, return all items in dir.

        Returns:
            list: List of file paths matching the pattern.
        """
        srch = p_file_pattern.split("*")
        files: list = []
        try:
            if Path(p_dir_path).exists() and Path(p_dir_path).is_dir():
                files = [f for f in Path(p_dir_path).iterdir()]
                if p_file_pattern != "":
                    files = [f for f in files if all(s in f.name for s in srch)]
        except Exception as err:
            raise (err)
        return files

    @classmethod
    def get_file(cls, p_path: str) -> str:
        """Read in an entire file and return its contents.
        We assume that this file type is text (string or bytes).

        Args:
            p_path (str): Legit path to file location.
        Return
            File content (Text))
        """
        content: str = ""
        try:
            if Path(p_path).exists():
                with open(p_path, "r") as f:
                    content = f.read().strip()
                f.close()
            return content
        except Exception as err:
            raise (err)

    @classmethod
    def get_numbers_data(cls, p_file_path: str, p_sheet_x: int = 0) -> pd.DataFrame:
        """Read data from Numbers (MacOS) spreadsheet tab
        and return as a DataFrame.

        Move to io_file.py

        :args:
        - p_file_path (str): Path to the workbook.
        - p_sheet_x (int): Index of sheet to load.
        :return:
        - (DataFrame): DataFrame of the sheet.
        """
        dataf = None
        doc = NumbersDoc(p_file_path)
        sheets = doc.sheets
        tables = sheets[p_sheet_x].tables
        data = tables[0].rows(values_only=True)
        dataf = pd.DataFrame(data[1:], columns=data[0])
        return dataf

    def get_spreadsheet_data(self, p_file_path: str, p_sheet: str = "") -> pd.DataFrame:
        """Get data from Excel, ODF, CSV (tab), or MacOS Numbers spreadsheet.
        Preference is for CSV files.

        :args:
        - p_file_path (str): Path to the workbook.
        - p_sheet (str): Name or Index of sheet to load. Optional.
            If it is a Numbers file, this needs to be an integer (index)
        :return:
        - (DataFrame): DataFrame of the sheet.
        """
        dataf = pd.DataFrame()
        ss_type = p_file_path.split(".")[-1].lower()
        sheet_nm = None if p_sheet == "" else p_sheet
        if ss_type.lower() in ("xlsx", "xls"):
            data = pd.read_excel(p_file_path, sheet_name=sheet_nm)
        elif ss_type.lower() in ("ods"):
            data = pd.read_excel(p_file_path, engine="odf", sheet_name=sheet_nm)
        elif ss_type.lower() in ("csv"):
            data = pd.read_csv(p_file_path)
        elif ss_type.lower() in ("numbers"):
            data = self.get_numbers_data(p_file_path, int(p_sheet))
        else:
            raise ValueError(f"{self.A['M']['file']}: {p_file_path}")
        if isinstance(data, pd.DataFrame):
            dataf = data
        return dataf

    @classmethod
    def is_file_or_dir(cls, p_path: str) -> bool:
        """Check if file or directory exists.
        Args:
            p_path (str): Legit path to file or dir location.
        Return
            True or False
        """
        if Path(p_path).exists():
            return True
        else:
            return False

    @classmethod
    def get_json_file(cls, p_path: str):
        """Read in an entire JSON file and return its contents as dict.

        Args:
            p_path (str): Legit path to JSON file location.
        Return
            File content (Dict or None)
        """
        content = None
        try:
            content = json.loads(cls.get_file(p_path))
            return content
        except Exception as err:
            raise (err)

    @classmethod
    def unpickle_object(cls, p_path: str):
        """Unpickle an object.
        Args:
            p_path: Legit path to pickled object location.
        Return:
            Unpickled Object or None
        """
        obj = None
        try:
            with open(p_path, "rb") as f:
                # trunk-ignore(bandit/B301)
                obj = pickle.load(f)
        except Exception as err:
            raise (err)
        return obj

    # Write methods
    # ==============================================================
    @classmethod
    def make_dir(cls, p_path: str):
        """Create directory at specified location.

        Success if directory already exists.

        Args:
            p_path: Legit path to create dir.
        """
        if not Path(p_path).exists():
            try:
                # trunk-ignore(bandit/B605)
                system(f"mkdir {p_path}")
            except Exception as err:
                raise (err)
        if not Path(p_path).exists():
            raise Exception(f"{p_path} directory creation failed.")

    @classmethod
    def delete_file(cls, p_path: str):
        """Remove a file.

        Args:
            p_path: Valid path to file to be removed.
        """
        try:
            remove(p_path)
        except OSError as err:
            raise (err)

    @classmethod
    def copy_one_file(cls, p_path_from: str, p_path_to: str):
        """Copy one file from source to target.

        Args:
            p_path_from (str): full path of file to be moved
            p_path_to (str): destination path
        """
        try:
            shutil.copy2(p_path_from, p_path_to)
        except OSError as err:
            raise (err)

    @classmethod
    def copy_all_files(cls, p_path_from: str, p_path_to: str):
        """Copy all files in dir from source to target.

        Args:
            p_path_from (str): full path of a dir with files to be moved
            p_path_to (str): destination path
        """
        try:
            cmd = f"cp -rf {p_path_from}/* {p_path_to}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise (msg)
        except Exception as err:
            raise (err)

    @classmethod
    def make_link(cls, p_link_from: str, p_link_to: str):
        """Make a symbolic link from the designated file
           at the requested destination.

        Args:
            p_link_from: path of file to be linked from
            p_link_to: destination path of the link
        """
        try:
            symlink(p_link_from, p_link_to)
        except OSError as err:
            raise (err)

    @classmethod
    def append_file(cls, p_path: str, p_text: str):
        """Append text to specified text file.

        Create file if it does not already exist.

        Args:
            p_path: Legit path to a text file location.
            p_text: Text to append to the file.
        """

        try:
            f = open(p_path, "a+")
            f.write(p_text)
            f.close()
        except Exception as err:
            raise (err)

    @classmethod
    def write_file(cls, p_path: str, p_data, p_file_type: str = "w+"):
        """Write or overwrite data to specified file.
        Create file if it does not already exist.

        Args:
            p_path (str): Legit path to a file location.
            p_data (str): Text to append to the file.
            p_file_type (str): default = "w+"
        """
        try:
            f = open(p_path, p_file_type)
            f.write(p_data)
            f.close()
        except Exception as err:
            raise (err)

    @classmethod
    def write_df_to_csv(cls, p_df: pd.DataFrame, p_csv_path: str):
        """Save dataframe as CSV.

        :args:
        - p_df (DataFrame): Dataframe to save as CSV.
        - p_csv_path (str): Path to the CSV file to create.
        """
        p_df.to_csv(p_csv_path, index=False)

    @classmethod
    def pickle_object(cls, p_path: str, p_obj):
        """Pickle an object.

        Args:
            p_path: Legit path to target object/file location.
            p_obj (obj): Object to be pickled (source)."""
        try:
            with open(p_path, "wb") as obj_file:
                pickle.dump(p_obj, obj_file)
        except Exception as err:
            raise (err)

    # CHMOD methods
    # ==============================================================
    @classmethod
    def make_readable(cls, p_path: str):
        """Make file at path readable for all.

        Args:
            p_path: File to make readable.
        """
        try:
            cmd = f"chmod u=rw,g=r,o=r {p_path}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise (msg)
        except Exception as err:
            raise (err)

    @classmethod
    def make_writable(cls, p_path: str):
        """Make file at path writable for all.

        Args:
            p_path: File to make writable.
        """
        try:
            cmd = f"chmod u=rwx,g=rwx,o=rwx {p_path}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise (msg)
        except Exception as err:
            raise (err)

    @classmethod
    def make_executable(cls, p_path: str):
        """Make file at path executable for all.

        Args:
            p_path: File to make executable.
        """
        try:
            cmd = f"chmod u=rwx,g=rx,o=rx {p_path}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise (msg)
        except Exception as err:
            raise (err)

    # Shaping and analysis methods
    # ==============================================================

    @classmethod
    def get_df_col_names(cls, p_df: pd.DataFrame) -> list:
        """Get list of column names from a dataframe.
        :args:
        - p_df (DataFrame): pandas dataframe to analyze
        """
        return list(p_df.columns.values)

    @classmethod
    def get_df_col_unique_vals(cls, p_col: str, p_df: pd.DataFrame) -> list:
        """For a dataframe column, return list of unique values.
        :args:
        - col_nm (str): Column name to get unique values for
        - s_df (DataFrame): Dataframe to process
        :returns:
        - (list): Unique values in column
        """
        u_vals = pd.DataFrame()
        u_vals = p_df.dropna(subset=[p_col])
        u_vals = u_vals.drop_duplicates(subset=[p_col], keep="first")
        vals: list = []
        if len(u_vals) > 1:
            vals = u_vals[p_col].values.tolist()
        vals.sort()
        return vals

    @classmethod
    def get_df_metadata(cls, p_df: pd.DataFrame) -> dict:
        """Get metadata from a dataframe:
        - Count of rows in dataframe.
        - Column names.
        - Unique values for each column.
        Assumes that column headers are on line 1 (index 0) of df.
        :args:
        - s_df (DataFrame): Dataframe being processed
        :returns:
        - (list): Unique values in column(s) or None
        """
        df = p_df.copy()
        df_meta = {"row_cnt": 0, "columns": {}}
        df_meta["row_count"] = len(df.index)
        cols = cls.get_df_col_names(df)
        for col_nm in cols:
            df_meta["columns"][col_nm] = cls.get_df_col_unique_vals(col_nm, df)
        return df_meta

    @classmethod
    def diff_files(cls, p_file_a: str, p_file_b: str) -> str:
        """Diff two files and return the result.
        :args:
        - p_file_a (str): full path to file A
        - p_file_b (str): full path to file B
        """
        try:
            cmd = f"diff {p_file_a} {p_file_b}"
            ok, msg = SM.run_cmd(cmd)
            if not ok:
                raise (msg)
            return msg
        except Exception as err:
            raise (err)
