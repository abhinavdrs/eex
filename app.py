"""
Run this app to generate reports
"""
from eex.margin_checker import MarginChecker
from eex.data import CI050, CC050


def compare():
    # init comparison object
    reporting_date = '2020-05-12'
    compare_obj = MarginChecker(reporting_date, CC050, CI050)
    write_report = compare_obj.write_assessed_report_to_csv()

if __name__ == "__main__":
    compare()