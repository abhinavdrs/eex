"""
Run this app to generate reports
"""

from margin_checker.logic import MarginChecker
from data import CI050, CC050

def compare():
    """
    Initialize a margin_checker object to generate and send report via email.

    :return: None
    """
    # init margin_checker object
    reporting_date = '2020-05-12'
    compare_obj = MarginChecker(reporting_date, CC050, CI050)
    compare_obj.assess_report()

    # generate individual reports to .csv
    compare_obj.write_assessed_report_to_csv()

if __name__ == "__main__":
    compare()
