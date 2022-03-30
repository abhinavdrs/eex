import datetime
from datetime import timedelta
import logging
import pandas as pd
from eex.conf.config import conf
from eex.send_report.logic import EmailReport

class MarginChecker:
    """
    comapares input CC an CI reports for a given date.
    """
    def __init__(self, date, cc050, ci050):
        """

        :param date:
        :param cc050:
        :param ci050:
        """
        self.reporting_date = self.parse_date(date)
        self.previous_date = self.reporting_date - timedelta(days=1)
        self.logger = self.initialize_logger()
        self.ci050 = ci050
        self.cc050 = cc050
        self.cc_entries = self.find_yesterday_cc_entries()
        self.sod_ci_entries = self.find_sod_ci_entries()
        self.eod_ci_entries = self.find_eod_ci_entries()
        self.report = self.generate_reports()
        self.assessed_report = self.assess_report()
        EmailReport(self.report_file)




    def initialize_logger(self):
        """

        :return: logger object
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

        self.report_file = f"report_{self.reporting_date}_{datetime.datetime.now().time()}.log"
        logfile_handler = logging.FileHandler(self.report_file)
        logfile_handler.setFormatter(formatter)

        logger.addHandler(logfile_handler)

        return logger

    def find_yesterday_cc_entries(self):
        """
        Finds entries from CC050 file for the day before.
        :return: list of lists
        """
        cc_entries = []
        for entry in self.cc050:
            if entry[0] == str(self.previous_date) and entry[3] in conf.margin_type_list:
                cc_entries.append(entry)
        return cc_entries

    def find_sod_ci_entries(self):
        """
        Finds start of day entries from CI050 file for the reporting day.
        :return: list of lists
        """
        sod_ci_entries = []
        for entry in self.ci050:
            if entry[0] == str(self.reporting_date) and entry[1] == '08:00:00' \
                    and entry[4] in conf.margin_type_list:
                sod_ci_entries.append(entry)

        return sod_ci_entries

    def find_eod_ci_entries(self):
        """
        Finds end of day entries from CI050 file for the day before.
        :return: list of lists
        """
        eod_ci_entries = []
        for entry in self.ci050:
            if entry[0] == str(self.previous_date) and entry[1] == '19:00:00' \
                    and entry[4] in conf.margin_type_list:
                eod_ci_entries.append(entry)

        return eod_ci_entries

    def find_closest_entry(self, list, name1, LOL, name2):
        """

        :param list: list
        :param name1:
        :param LOL:
        :param name2:
        :return:
        """
        conflict_map = []

        for i, value in enumerate(list):
            in_list = set(value[0])
            print(f"in_list:{in_list}, value[0] {value[0]}, value[1]{value[1]}")
            closest_entry = [entry for entry in LOL if len(in_list - set(entry)) == 1]
            for entry in closest_entry:
                diff_set = set(in_list) - set(entry)
                is_float = self.if_float(diff_set.pop())
                if is_float:
                    index_closes_entry = LOL.index(entry)
                    conflict_map.append((value[1], index_closes_entry))
                    print(f"conflicted entry for list:{name1}:{value} is {name2}{entry}")

        # print(conflict_map)
        return conflict_map

    def cc_with_sod_ci(self):
        """
        compares CC050 with SOD CI

        :return: dict
        """
        ret_dict = self.compare_two_lol(self.cc_entries, f"CC050_{self.previous_date}",
                                        self.sod_ci_entries, f"CI050_{self.reporting_date}")

        return {conf.cc_with_sod_ci: ret_dict}

    def cc_with_eod_ci(self):
        """
        compares CC050 with EOD CI

        :return: dict
        """
        ret_dict = self.compare_two_lol(self.cc_entries, f"CC050_{self.previous_date}",
                                        self.eod_ci_entries, f"CI050_{self.previous_date}")

        return {conf.cc_with_eod_ci: ret_dict}

    def ci_eod_with_sod(self):
        """
        compares EOD CI with SOD CI
        :return: dict
        """
        ret_dict = self.compare_two_lol(self.eod_ci_entries, f"CI050_{self.previous_date}",
                                        self.sod_ci_entries, f"CI050_{self.reporting_date}")

        return {conf.ci_eod_with_sod: ret_dict}

    def generate_reports(self):
        """
        Generate consolidated report for all three classes of comparisons
        :return:
        """
        report_dict = {}
        report_dict.update(self.cc_with_sod_ci())
        report_dict.update(self.cc_with_eod_ci())
        report_dict.update(self.ci_eod_with_sod())

        self.report = {f"report_{self.reporting_date}": report_dict}

        return {f"report_{self.reporting_date}": report_dict}

    def assess_report(self):
        """

        :return: A dictionary of assessed records.
        """
        assessed_report = {}
        print(f"analyzing: {self.report[f'report_{self.reporting_date}']}")
        # compare CC_wth_SOD
        report_keys = self.report[f'report_{self.reporting_date}'].keys()

        key_to_name_map = {
                           'cc_with_sod_ci':{'name1':'CC050',
                                             'name2':'CI050_sod',
                                             'lists':[self.cc_entries, self.sod_ci_entries]
                                             },
                           'cc_with_eod_ci':{'name1':'CC050',
                                             'name2':'CI050_eod',
                                             'lists':[self.cc_entries, self.eod_ci_entries]},
                           'ci_eod_with_sod':{'name1':'CI050_eod',
                                             'name2':'CI050_sod',
                                             'lists':[self.eod_ci_entries, self.sod_ci_entries]}
                           }

        for key in report_keys:
            print(f'key:{key} in report_keys:{report_keys}')

            name1 = key_to_name_map[key]['name1']
            name2 = key_to_name_map[key]['name2']
            lists = key_to_name_map[key]['lists']
            self.logger.info("\nComparing {name1} with {name2}...\n")

            print(f"testing dict logic name1: {name1}, name2:{name2}, lists:{lists}")
            report = self.report[f'report_{self.reporting_date}'][key]

            print("len(report['missing'][0])", len(report['missing'][0]))
            # entries present in 1 but not in 2
            missing_in_1 = [lists[0][entry] for entry in report['missing'][0]]
            missing_in_1_accounts = [entry[-2] for entry in missing_in_1]
            # write to logger
            [self.logger.error(f"Missing:entry:{entry} from {name1} is not found in {name2}") for entry in missing_in_1]
            [self.logger.error(f"Missing Margin Type:margin type:{account} from {name1} is not found in {name2}") for account in missing_in_1_accounts]

            conflict_1_2_tuples = report['conflict'][0]
            print(f'conflict_{name1}_{name2} for key {key}', conflict_1_2_tuples)
            conflict_1_2_values = []
            conflict_1_2_account = []

            if len(conflict_1_2_tuples):
                conflict_1_2_values = [(lists[0][entry[0]], lists[1][entry[1]])
                                       for entry in conflict_1_2_tuples]

                [self.logger.error(f"Conflicted_entry:{entry[0]} of {name1} is conflicted with entry:{entry[1]} of "
                                   f"{name2}") for entry in conflict_1_2_values]

                conflict_1_2_account = [(entry[0][-2], entry[0][-1], entry[1][-1])
                                        for entry in conflict_1_2_values]
                [self.logger.error(f"Conflicted Margin Type:Recorded margin for margin type:{entry[0]} is {entry[1]} in {name1}"
                                   f" but is {entry[2]} in {name2}")
                 for entry in conflict_1_2_account]

            # entries present in 2 but not in 1
            missing_in_2 = [lists[1][entry] for entry in report['missing'][1]]
            missing_in_2_accounts = [entry[-2] for entry in missing_in_2]
            [self.logger.error(f"Missing:entry:{entry} from {name2} is not found in {name1}") for entry in missing_in_2]
            print(f'missing_in_{name2} for key {key}', missing_in_2)
            print(f'missing_in_{name2}_accounts for key {key}', missing_in_2_accounts)
            [self.logger.error(f"Missing Margin Type:margin type:{account} from {name2} is not found in {name1}") for account in
             missing_in_2_accounts]



            # conflicted entries of 2 with 1
            conflict_2_1_tuples = report['conflict'][1]
            print(f'conflict_{name2}_{name1} for key {key}', conflict_2_1_tuples)
            conflict_2_1_values = []
            conflict_2_1_account = []
            if len(conflict_2_1_tuples):
                conflict_2_1_values = [(lists[1][entry[0]], lists[0][entry[1]])
                                       for entry in conflict_2_1_tuples]
                [self.logger.error(f"Conflicted_entry:{entry[0]} of {name2} is conflicted with entry:{entry[1]} of"
                                   f" {name1}")
                 for entry in conflict_2_1_values]
                conflict_2_1_account = [(entry[0][-2], entry[0][-1], entry[1][-1])
                                        for entry in conflict_2_1_values]
                [self.logger.error(f"Conflicted Margin Type:Recorded margin for margin type {entry[0]} is {entry[1]} in {name2}"
                                   f" but is {entry[2]} in {name1}")
                 for entry in conflict_1_2_account]
                print(f'conflict_{name2}_{name1}_values for key {key}', conflict_2_1_values)
                print(f'conflict_{name2}_{name1}_accounts for key {key}', conflict_2_1_account)

            entry_report = {f"Accounts_in_{name1}_missing_From_{name2}": missing_in_1_accounts,
                            f"Entries_in_{name1}_missing_from_{name2}": missing_in_1,
                            f"Conflicted_Account_Name, val_in_{name1}, val_in_{name2}": conflict_1_2_account,
                            f"Accounts_in_{name2}_missing_From_{name1}": missing_in_2_accounts,
                            f"Entries_in_{name2}_missing_from_{name1}": missing_in_2,
                            f"Conflicted_Account_Name, val_in_{name2}, val_in_{name1}": conflict_2_1_account,
                            }
            assessed_report[key] = entry_report

        # self.assessed_report = assessed_report
        return assessed_report

    def write_assessed_report_to_csv(self):
        """
        Dumps the contents of self.assessed_report to three .csv files.
        :return:  bool: True if write to .csv successfull.
        """

        ret = False
        for key in self.assessed_report.keys():
            try:
                data_frame = pd.json_normalize(self.assessed_report[key])
            except Exception as exc:
                print(f"Failed to write to .csv. Exception:{exc} occurred.")
            else:
                data_frame.to_csv(f"{key}.csv", mode='w', index=None, header=True)
                ret = True
        return ret

    def compare_two_lol(self, lol_1, name1, lol_2, name2):
        """
        The function compares two input LOL. The function does not assume the LOL to be of same length.
        The returned dict contains all findings neccessary for reporting.

        :param lol_1: List of Lists of input report 1.
        :param name1: name of input report 1
        :param lol_2: List of Lists of input report 2.
        :param name2: name of input report 2.
        :return: dictionary with both comparisons
        """

        # lol_1 last 4 entries
        lol1_last_4_entries = [entry[-4:] for entry in lol_1]

        # lol_2 of last 4 entries
        lol2_last_4_entries = [entry[-4:] for entry in lol_2]

        # set logic to find entries in lol1 but missing in lol2
        difference1_2 = set(tuple(row) for row in lol1_last_4_entries) - \
                        set(tuple(row) for row in lol2_last_4_entries)
        tol_missing_entries_lol1 = []
        tuple_missing_entries_lol1 = []

        for row in difference1_2:
            index = lol1_last_4_entries.index(list(row))
            tol_missing_entries_lol1.append((lol_1[index][-4:], index))
            tuple_missing_entries_lol1.append(index)

        conflict_report_1_2 = self.find_closest_entry(tol_missing_entries_lol1, name1, lol2_last_4_entries, name2)

        difference2_1 = set(tuple(row) for row in lol2_last_4_entries) - \
                        set(tuple(row) for row in lol1_last_4_entries)
        tol_missing_entries_lol2 = []
        tuple_missing_entries_lol2 = []
        for row in difference2_1:
            index = lol2_last_4_entries.index(list(row))
            tol_missing_entries_lol2.append((lol_2[index][-4:], index))
            tuple_missing_entries_lol2.append(index)

        conflict_report_2_1 = self.find_closest_entry(tol_missing_entries_lol2, name2, lol1_last_4_entries, name1)

        lol1_vs_lol2 = {"report1": name1,
                        "report2": name2,
                        "missing": [tuple_missing_entries_lol1, tuple_missing_entries_lol2],
                        "conflict": [conflict_report_1_2, conflict_report_2_1]
                        }

        return lol1_vs_lol2

    @staticmethod
    def parse_date(date):
        """

        :param date: Date in YYYY-MM-DD
        :return: datetime object
        """
        try:
            ret = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except Exception as exc:
            print("Incorrect Date Format. Please use YYYY-MM-DD")
            raise exc
        else:
            return ret

    @staticmethod
    def if_float(value):
        """

        :param value: any datatype
        :return: bool: True if value is float else false.
        """
        is_float = False
        try:
            float(value)
        except Exception as exc:
            print(f"Exception {exc} in is_float")
        else:
            is_float = True

        return is_float
