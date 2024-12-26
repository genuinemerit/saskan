#! python
"""Saskan logger and monitor functions.
:module:    wiretap.py
:class:     Logger/0
:author:    GM <genuinemerit @ pm.me>

*** Mostly AI-generated code. Review and test carefully.  ***

@DEV:
- Monitoring functions would be more analysis-oriented, based on log data.
- What should be monitored and how. Would there be throttles and alerts?

### Detailed Explanation

- **SQLiteHandler:** A custom logging handler that logs to an SQLite database.

  - **emit():** Overrides the `emit` method of `Handler` to log records to the database.

- **DatabaseLogger**: Manages logging operations using standard Python logging modules,
  with output directed to an SQLite database.

  - **Methods Available:**

    - `set_log_level(level)`: Adjusts the logging level.

    - `set_log_format(format)`: Adjusts the logging format.

    - Logging methods (`debug`, `info`, `warning`, `error`, `critical`)
        are provided to log messages at various severities.

    - `query_logs()`: Retrieves log records from the database.

    - `clear_logs()`: Deletes all existing logs.

- **Logging Format and Handling Exceptions:** The `DatabaseLogger` facilitates
   a flexible format string, efficiently converts log levels and timestamps,
   and resolves exceptions within the log record.

This design assumes a robust `DataBase` class that handles all database operations
  efficiently and safely, taking the responsibility of maintaining database connections
  and transactions.
"""
import logging
from logging import Handler, LogRecord
from data_base import DataBase
from method_files import FileMethods
from method_shell import ShellMethods

FM = FileMethods()
SM = ShellMethods()


class SQLiteHandler(Handler):
    """
    SQLite logging handler for inserting logging records into an SQLite database table.
    @DEV:
    - May  want to move this to the set_data module, but since it is so closely
      tied to logging might be OK to leave it here.
    """

    def __init__(self):
        """
        Initialize the IO handler.

        :param db: An instance of the DataBase class to handle database operations.
        """
        super().__init__()
        self.CONTEXT = FM.get_json_file("static/context/context.json")
        self.USERDATA = FM.get_json_file("static/context/userdata.json")
        self.DB = DataBase(self.CONTEXT)

    def emit(self, record: LogRecord):
        """
        Emit a record.

        Insert the log record into the LOGS table within the database.

        :param record: A LogRecord object containing all the pertinent information.
        """
        try:
            # Format record
            log_time = self.formatTime(record, SM.get_iso_time_stamp())
            log_level = record.levelname
            message = self.formatMessage(record)
            exception_info = (
                self.formatException(record.exc_info) if record.exc_info else "None"
            )

            # Can we use traceback here to capture the stack trace if there was an exception?

            # Insert into database
            self.DB.execute_insert(
                "LOGS", (SM.get_uid(), log_time, log_level, message, exception_info)
            )
        except Exception as e:
            print(e)
            self.handleError(record)


class Logger:
    """
    A logging facade for logging into an SQLite database using the logging facility.
    For log level constants, see data_structs: LogLevel.

    @NB:
    - According to ChatGPT, setting exc_info=True in logging call will include
      trace info in the log record.
      Play with that before trying to implement a "trace on/off" feature.

    @DEV:
    - In the CLI or GUI front-ends, provide methods set logging level, etc.
    - Add an option to turn traceback on or off.
    - Also should have options to view logs in the GUI or CLI and to clear logs.
    """

    def __init__(self, name: str = __name__):
        """
        Initialize the database logger.

        :param name: The name of the logger.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Default level is DEBUG
        self.handler = SQLiteHandler()
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
            + "- %(classname)s - %(funcName)s - %(lineno)d"
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def set_log_level(self, level: int):
        """
        Set the logging level.

        :param level: The logging level to be set.
        """
        self.logger.setLevel(level)

    def set_log_format(self, format: str):
        """
        Set the logging format.

        @DEV: This may not be necessary if the format is set by configuration.

        :param format: The logging format to be set.
        """
        self.formatter = logging.Formatter(format)
        self.handler.setFormatter(self.formatter)

    def debug(self, message: str, *args, **kwargs):
        """
        Log a message with severity 'DEBUG'.

        :param message: The log message.
        """
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """
        Log a message with severity 'INFO'.

        :param message: The log message.
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """
        Log a message with severity 'WARNING'.

        :param message: The log message.
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, exc_info=False, **kwargs):
        """
        Log a message with severity 'ERROR'.

        :param message: The log message.
        :param exc_info: Specifies that exception information
            should be added to the logging message.
        """
        self.logger.error(message, *args, exc_info=exc_info, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """
        Log a message with severity 'CRITICAL'.

        :param message: The log message.
        """
        self.logger.critical(message, *args, **kwargs)

    def query_logs(self):
        """
        Query and return the logs from the LOGS table.

        :return: Query result as a list of log entries.
        """
        # Assuming that database class provides a way to execute a select
        # query and return results.
        # @DEV: Implement this method using appropriate DB call.
        return self.db.execute_select("SELECT * FROM LOGS")

    def clear_logs(self):
        """
        Clear all logs from the LOGS table.
        @DEV:
        - This should have an option to select logs older than x days.
        - May also want an "are you sure?" prompt.
        """
        # Using a simple execute statement to clear existing logs.
        # @DEV: Implement this method using appropriate DB call(s).
        self.db.execute_delete("DELETE FROM LOGS")
