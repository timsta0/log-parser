# log-parser
Parser for .log files. Log files for testing are located in sample_files diresctory.
## supported format of logs
```
2021-03-19 11:39:38,730 - mf - INFO - Using configuration 'DefaultConfiguration'
```
or
```
2021-03-19 11:40:42,600 - mf - INFO - Parameters:
           only_file=True
           mypackage.show_report=
```
## executing tests
```
python3 tests.py
```
