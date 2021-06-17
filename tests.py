import unittest
from log_parser import *


class ParserTest(unittest.TestCase):
    def setUp(self):
        """
        Setup for all .log files
        """
        self.oneLineProcessor = LogEntryProcessor(
            "./sample_files/single_line_sample.log"
        )
        self.multiLineProcessor = LogEntryProcessor(
            "./sample_files/multi_line_sample.log"
        )
        self.multiLineProcessorWhitespace = LogEntryProcessor(
            "./sample_files/multi_line_whitespace_sample.log"
        )
        self.notSupportedProcessor = LogEntryProcessor(
            "./sample_files/not_supported_format.log"
        )
        self.emptyProcessor = LogEntryProcessor("./sample_files/empty_sample.log")
        self.emptyFileName = LogEntryProcessor("")
        self.doesNotExist = LogEntryProcessor("./sample_files/i_do_not_exist.log")
        self.notLogFile = LogEntryProcessor("./sample_files/log_file.txt")
        print("RUNNING... TEST:", unittest.TestCase.shortDescription(self))


class LogParserTests(ParserTest):
    def test01_simple_log_file(self):
        "Parsing single-line log file."
        self.oneLineProcessor.parse()
        assert len(self.oneLineProcessor.get_entries()) == 14

    def test02_multi_line_log_file(self):
        "Parsing multi-line log file."
        self.multiLineProcessor.parse()
        assert len(self.multiLineProcessor.get_entries()) == 16

    def test03_empty_file_parsing(self):
        "Parsing an empty file."
        self.emptyProcessor.parse()
        assert (len(self.emptyProcessor.get_entries())) == 0

    def test04_multi_line_log_file_whitespace(self):
        "Parsing multi-line log file with whitespace at first line."
        self.multiLineProcessorWhitespace.parse()
        assert len(self.multiLineProcessorWhitespace.get_entries()) == 14

    def test05_empty_file_name(self):
        'Parsing file with name "".'
        self.assertRaises(FileNotFoundError, self.emptyFileName.parse)

    def test06_file_does_not_exist(self):
        "Parsing file that does not exist."
        self.assertRaises(FileNotFoundError, self.doesNotExist.parse)

    def test07_not_a_log_file(self):
        "Parsing file with wrong extension."
        self.assertRaises(FormatNotSupported, self.notLogFile.parse)

    def test06_format_not_supported_error(self):
        "Parsing not supported log format should raise an error."
        self.assertRaises(FormatNotSupported, self.notSupportedProcessor.parse)

    def test07_entries_not_parsed(self):
        "Get entries without parsing should raise an error."
        self.assertRaises(NotParsedError, self.oneLineProcessor.get_entries)


class SeverityFilterFunctionality(ParserTest):
    def test01_filter_by_severity_entries(self):
        "Filter by severity single-line log file."
        self.oneLineProcessor.parse()
        severity_entries = self.oneLineProcessor.get_severity_entries("INFO")
        assert len(severity_entries) == 5
        for entry in severity_entries:
            assert entry.severity == "INFO"

    def test02_filter_by_severity_multi_line(self):
        "Filter by severity multi-line log file."
        self.multiLineProcessor.parse()
        severity_entries = self.multiLineProcessor.get_severity_entries("INFO")
        assert len(severity_entries) == 7
        for entry in severity_entries:
            assert entry.severity == "INFO"

    def test03_filter_by_severity_empty_file(self):
        "Filtering an empty log file by severity."
        self.emptyProcessor.parse()
        severity_entries = self.emptyProcessor.get_severity_entries("INFO")
        assert severity_entries == []

    def test04_filter_by_severity_not_parsed_entries(self):
        "Filtering by severity without parsing should raise an error."
        self.assertRaises(
            NotParsedError, self.oneLineProcessor.get_severity_entries, "INFO"
        )


class NameFilterFunctionality(ParserTest):
    def test01_filter_by_name_entries(self):
        "Filter by name simple log file."
        self.oneLineProcessor.parse()
        name_entries = self.oneLineProcessor.get_named_entries("mf")
        assert len(name_entries) == 10
        for entry in name_entries:
            assert entry.logger_name == "mf"

    def test02_filter_by_name_multi_line(self):
        "Filter by name multi-line log file."
        self.multiLineProcessor.parse()
        name_entries = self.multiLineProcessor.get_named_entries("mf")
        assert len(name_entries) == 12
        for entry in name_entries:
            assert entry.logger_name == "mf"

    def test03_filter_by_name_empty_file(self):
        "Filtering an empty log file by name."
        self.emptyProcessor.parse()
        name_entries = self.emptyProcessor.get_named_entries("mf")
        assert name_entries == []

    def test04_filter_by_name_not_parsed_entries(self):
        "Filtering by name without parsing should raise an error."
        self.assertRaises(NotParsedError, self.oneLineProcessor.get_named_entries, "mf")


class SubstringFilterFunctionality(ParserTest):
    def test01_filter_by_substring_entries(self):
        "Filter by substring simple log file."
        self.oneLineProcessor.parse()
        substring_entries = self.oneLineProcessor.get_entries_with_substring("file")
        assert len(substring_entries) == 3
        for entry in substring_entries:
            assert "file" in entry.message

    def test02_filter_by_substring_multi_line(self):
        "Filter by substring multi-line log file."
        self.multiLineProcessor.parse()
        substring_entries = self.multiLineProcessor.get_entries_with_substring("file")
        assert len(substring_entries) == 4
        for entry in substring_entries:
            assert "file" in entry.message

    def test03_filter_by_substring_empty_file(self):
        "Filtering an empty log file by substring."
        self.emptyProcessor.parse()
        substring_entries = self.emptyProcessor.get_entries_with_substring("mf")
        assert substring_entries == []

    def test04_filter_by_substring_not_parsed_entries(self):
        "Filtering by substring without parsing should raise an error."
        self.assertRaises(
            NotParsedError, self.oneLineProcessor.get_entries_with_substring, "file"
        )


class TimestampFilterFunctionality(ParserTest):
    def test01_filter_by_timestamp_entries(self):
        "Get newer entries from simple log file."
        self.oneLineProcessor.parse()
        timestamp_entries = self.oneLineProcessor.get_newer_entries(
            "2021-03-19 11:39:39,286"
        )
        assert len(timestamp_entries) == 6
        for entry in timestamp_entries:
            assert entry.timestamp > "2021-03-19 11:39:39,286"

    def test02_filter_by_timestamp_multi_line(self):
        "Get newer entries from multi line log file"
        self.multiLineProcessor.parse()
        timestamp_entries = self.multiLineProcessor.get_newer_entries(
            "2021-03-19 11:39:39,286"
        )
        assert len(timestamp_entries) == 8
        for entry in timestamp_entries:
            assert entry.timestamp > "2021-03-19 11:39:39,286"

    def test03_filter_by_timestamp_empty_file(self):
        "Get newer entries from an empty file."
        self.emptyProcessor.parse()
        timestamp_entries = self.emptyProcessor.get_newer_entries(
            "2021-03-19 11:39:39,286"
        )
        assert timestamp_entries == []

    def test04_filter_by_timestamp_not_parsed_entries(self):
        "Getting newer entries without parsing should raise an error."
        self.assertRaises(
            NotParsedError,
            self.oneLineProcessor.get_newer_entries,
            "2021-03-19 11:39:39,286",
        )

    def test05_filter_by_timestamp_wrong_timestamp(self):
        "Getting newer entries with wrong timestamp format should raise an error."
        self.assertRaises(
            FormatNotSupported, self.oneLineProcessor.get_newer_entries, "01-10-2020"
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
