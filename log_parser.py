import re
import os.path


class LogEntry:
    "This class represents one log entry."

    def __init__(self, timestamp, logger_name, severity, message):
        """
        Init
        :param timestamp:   string
        :param logger_name: string
        :param severity:    string
        :param message:     string, log message
        """
        self.timestamp = timestamp
        self.logger_name = logger_name
        self.severity = severity
        self.message = message


class LogEntryProcessor:
    "This class represents an array of entries and is used for log file parsing and filtering log entries."

    def __init__(self, filename):
        """
        Init
        :param filename:    string
        """
        self.filename = filename
        self.entries = []
        self.isParsed = False
        self.pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} - .* - [A-Z]* - *"

    def parse(self):
        """
        Class method for parsing.
        If file is an emptry string or file does not exist then FileNotFoundError is raised.
        If file has wrong extention then FormatNotSupported is raised.
        Sets entries and isParsed flag as True if parsing is successful.
        """
        if self.filename == "":
            raise FileNotFoundError("Missing a file name.")
        elif not os.path.isfile(self.filename):
            raise FileNotFoundError("File does not exist.")
        elif not self.filename.endswith(".log"):
            raise FormatNotSupported("This is not a .log file.")
        with open(self.filename, "r") as file:
            for line in file:
                if line[0].isspace():
                    if self.entries == []:
                        entry = LogEntry(None, None, None, line)
                        self.entries.append(entry)
                    else:
                        self.entries[-1].message += line
                    continue
                if not re.match(self.pattern, line):
                    raise FormatNotSupported("Log file format is not supported.")
                line = line.split(" - ", 3)
                entry = LogEntry(line[0], line[1], line[2], line[3])
                self.entries.append(entry)
        self.isParsed = True

    def get_entries(self):
        """
        Class method that returns array of LogEntry objects.
        If file was not  parsed then exception is raised.
        """
        if not self.isParsed:
            raise NotParsedError("File is not parsed.")
        return self.entries

    def get_severity_entries(self, severity):
        """
        Class method for filtering entries by severity that returns array of LogEntry objects.
        If file was not parsed then exception is raised.

        :param severity     string
        """
        if not self.isParsed:
            raise NotParsedError("File is not parsed.")
        res = []
        for entry in self.entries:
            if entry.severity == severity:
                res.append(entry)
        return res

    def get_named_entries(self, name):
        """
        Class method for filtering entries by name that returns array of LogEntry objects.
        If file was not parsed then exception is raised.

        :param name         string
        """
        if not self.isParsed:
            raise NotParsedError("File is not parsed.")
        res = []
        for entry in self.entries:
            if entry.logger_name == name:
                res.append(entry)
        return res

    def get_entries_with_substring(self, substring):
        """
        Class method for filtering entries by substring in message that returns array of LogEntry objects.
        If file was not parsed then exception is raised.

        :param substring    string
        """
        if not self.isParsed:
            raise NotParsedError("File is not parsed.")
        res = []
        for entry in self.entries:
            if substring in entry.message:
                res.append(entry)
        return res

    def get_newer_entries(self, timestamp):
        """
        Class method for filtering entries by timestamp that returns array of LogEntry objects with newer timestamps.
        If file was not parsed or timestamp is in a different format then exception is raised.

        :param timestamp    string
        """
        if not re.match(
            "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}", timestamp
        ):
            raise FormatNotSupported("Timestamp format not supported.")
        if not self.isParsed:
            raise NotParsedError("File is not parsed.")
        for i in range(len(self.entries)):
            if self.entries[i].timestamp > timestamp:
                return self.entries[i : len(self.entries)]
        return []


class NotParsedError(Exception):
    """
    Customed exception that is raised when file was not parsed.
    """

    pass


class FormatNotSupported(Exception):
    """
    Customed exception that is raised when format of file/timestamp is not supported.
    """

    pass
