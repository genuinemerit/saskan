#!/usr/bin/python3.9
"""
:module:    method_shell.py
:class:     ShellMethods/0
:author:    GM (genuinemerit @ pm.me)

Shell services and utilities.
- Service Activator / Deactivator class for Data Schema services.
- Generic system command runner.
- Some basic IO utilities so we don't have to import FileIO everywhere.
"""
import hashlib  # generate hash keys
import inspect  # getdoc
import pendulum  # Handle datetime with timezone
import platform
import secrets
import subprocess as shl
import traceback  # Exception trace

from collections import OrderedDict
from os import environ, path, system
from pathlib import Path


class ShellMethods(object):
    """Run Controller-related commands."""

    def __init__(self):
        """Initialize the object."""
        pass

    @classmethod
    def get_platform(cls) -> str:
        """Return platform information."""
        return platform.platform()

    @classmethod
    def get_key(cls) -> str:
        """Generate a cryptographically strong key."""
        return secrets.token_urlsafe(32)

    @classmethod
    def get_datetime(cls, timezone="America/New_York"):
        """
        Get a pendulum datetime object for the specified timezone.

        :param timezone: The timezone to use for the datetime object.
                         Defaults to "America/New_York".
        :return: A pendulum datetime object.
        """
        return pendulum.now(timezone)

    @classmethod
    def get_iso_time_stamp(cls, timezone="America/New_York") -> str:
        """
        Get a timestamp in ISO 8601 format for the specified timezone.

        :param timezone: The timezone to use for the timestamp. Defaults to "America/New_York".
        :return: A timestamp string in ISO 8601 format.
        """
        return pendulum.now(timezone).to_iso8601_string()

    @classmethod
    def get_date_string(cls, p_date, p_date_format: str = "") -> str:
        """Get a date string in YYYY-MM-DD format.
        :param p_date: Date object or string
        :param p_date_format: Date format string
        """
        if p_date_format:
            p_date = pendulum.from_format(p_date, p_date_format)
        return p_date.to_date_string()

    @classmethod
    def get_hash(cls, p_data_in: str) -> str:
        """Create a SHA-512 hash of the input string.
        :param p_data_in: Input string to hash
        """
        v_hash = hashlib.sha512()
        v_hash.update(p_data_in.encode("utf-8"))
        return v_hash.hexdigest()

    @classmethod
    def get_uid(cls, p_uid_length: int = 32) -> str:
        """Generate a URL-safe, cryptographically strong random value.
        :param p_uid_length: Length of the UID
        """
        p_uid_length = max(p_uid_length, 32)
        exclude = {";", ":", "/", '"', "\\", "'", "?", "#", "|"}
        while True:
            uid_val = secrets.token_urlsafe(p_uid_length)
            if not any(char in uid_val for char in exclude):
                return uid_val

    @classmethod
    def remove_dups(cls, list_in: list) -> list:
        """Remove duplicates from a list.
        :param list_in: Input list
        """
        return list(dict.fromkeys(list_in))

    @classmethod
    def get_substring_exclusive(
        cls, full_str: str, from_token: str, to_token: str
    ) -> str:
        """
        Get a substring from a string, between two tokens,
        that is, exclusive of the tokens.

        :param full_str: The original string from which to extract the substring.
        :param from_token: The token after which the substring starts.
        :param to_token: The token before which the substring ends.
        :return: The substring found between the two tokens; returns an
                  empty string if tokens are not found.
        """
        try:
            start_index = full_str.index(from_token) + len(from_token)
            end_index = full_str.index(to_token, start_index)
            return full_str[start_index:end_index]
        except ValueError:
            # Return an empty string if from_token or to_token is not found
            return ""

    @classmethod
    def get_substring_inclusive(
        cls, full_str: str, from_token: str, to_token: str
    ) -> str:
        """
        Get a substring from a string, between two tokens,
        that is, inclusive of the tokens.

        :param full_str: The original string from which to extract the substring.
        :param from_token: The token where the substring starts (inclusive).
        :param to_token: The token where the substring ends (inclusive).
        :return: The substring found between the two tokens; returns an
                 empty string if tokens are not found.
        """
        try:
            start_index = full_str.index(from_token)
            end_index = full_str.index(to_token, start_index) + len(to_token)
            return full_str[start_index:end_index]
        except ValueError:
            # Return an empty string if from_token or to_token is not found
            return ""

    @classmethod
    def run_cmd(cls, cmd: str) -> tuple:
        """Execute a shell command from Python.
        :param cmd: Command to run
        """
        if not cmd:
            return False, ""

        try:
            shell = shl.Popen(
                cmd, shell=True, stdin=shl.PIPE, stdout=shl.PIPE, stderr=shl.STDOUT
            )
            cmd_result, _ = shell.communicate()
            cmd_rc = not any(
                keyword in cmd_result for keyword in (b"failure", b"fatal")
            )
            return cmd_rc, cmd_result.decode("utf-8").strip()
        except Exception as e:
            return False, str(e)

    @classmethod
    def run_nohup_py(cls, pypath, logpath, p1, p2, p3, log_nm):
        """Run a Python script in the background with no hangup.
        :param pypath: Path to the Python script including the script name
        :param logpath: Path to the log file, but not the log file name
        :param p1: Parameter 1 for the Python script
        :param p2: Parameter 2
        :param p3: Parameter 3
        :param log_nm: Log file name
        """
        cmd = (
            f"nohup python -u {pypath} '{p1}' {p2} {p3} > "
            f"{logpath}/{log_nm}_{p1.replace('/', '_').replace('__', '_')}.log 2>&1 &"
        )
        try:
            system(cmd)
        except Exception as err:
            raise Exception(f"{err} {cmd}")

    @classmethod
    def get_host(cls) -> str:
        """
        Get the hostname of the machine running the program.

        :return: The hostname as a string.
        """
        return platform.node()

    @classmethod
    def get_os_home(cls) -> str:
        """Get the home directory."""
        return environ.get("HOME", "")

    @classmethod
    def get_cwd_home(cls) -> str:
        """Derive the home directory from the current working directory."""
        cwd_parts = Path.cwd().parts
        return path.join("/home", cwd_parts[2]) if len(cwd_parts) > 2 else ""

    @classmethod
    def get_help(cls, p_class_obj: object, p_command: str):
        """Return docstring for a specific method within a class.
        :param p_class_obj: Class object
        :param p_command: Command/method within the Class object for which to get help
        """
        method = getattr(p_class_obj, p_command, None)
        return inspect.getdoc(method) if method else f"Command '{p_command}' not found."

    @classmethod
    def continue_prompt(cls) -> str:
        """Prompt user to continue or stop."""
        response = ""
        while response not in ("y", "n"):
            response = input("Continue? (y/n): ")
        return response

    @classmethod
    def convert_dict_to_ordered_dict(cls, p_dict: dict) -> OrderedDict:
        """
        Convert a dictionary to an ordered dictionary sorted by the 'order' key.

        :param p_dict: The input dictionary where each value is expected
                       to be a dictionary containing an 'order' key.
        :return: An OrderedDict sorted by the 'order' key of the inner dictionaries.
        """
        sorted_items = sorted(p_dict.items(), key=lambda item: item[1]["order"])
        return OrderedDict(sorted_items)

    @classmethod
    def show_trace(cls, e: Exception):
        """Display exception trace."""
        error_msg = f"{str(e)}"
        tb = e.__traceback__
        formatted_tb = traceback.format_exception(type(e), e, tb)
        error_msg += "\n" + ("".join(formatted_tb))
        return error_msg

    def rpt_running_jobs(self, p_job_nm: str):
        """Return display of running jobs matching grep param.
        :param p_job_nm: Job name to grep
        """
        ok, result = self.run_cmd(f"ps -ef | grep {p_job_nm}")
        if not ok:
            raise Exception(result)
        running_jobs = result.split("\n")
        return result, running_jobs

    def kill_jobs(self, p_job_nm: str):
        """Kill jobs matching job name param.
        :param p_job_nm: Job name to grep
        """
        _, running_jobs = self.rpt_running_jobs(p_job_nm.strip())
        for job in running_jobs:
            job_pid = job.split()[1].strip()
            self.run_cmd(f"kill -9 {job_pid}")
