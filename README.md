### Margin Checker
A simple python application to compare lists of lists and compare a subset of their elements.

### Instructions for running with sample data:
1) Clone repository in your favourite IDE
2) pip install -r requirements.txt
3) python3 app.py

### Instructions for running with own data.
1) Initialize object for MarginChecker class.
    1) The MarginChecker class accepts reporting_date, End of day report (CC050) entries and Intraday report (CI050) Entries as arguments.
    2) Please provide these entries as List Of Lists as shown in data.py
    3) Once initialized the MarginChecker object will perform comparison and send error report to configured emails in config.yaml.
 
 2) Additional info:
    1) The margin_types are configurable and can be added/removed from config.yaml
    2) MarginChecker function write_assessed_report_to_csv() can be used to write local .csv file of three reports.
    
 




