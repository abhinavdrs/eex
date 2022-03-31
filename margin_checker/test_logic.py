import pytest
from margin_checker.logic import MarginChecker
from unittest.mock import Mock
from mock import patch
mock = Mock()


CC050 = [['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2]]
CI050 = [['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
         ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2]
         ]

CC050_2 = []
CI050_2 = []

CC050_3 = [['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.3]]
CI050_3 = [['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
           ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'SPAN', 3212.4]
           ]


@pytest.mark.parametrize("test_input1, expected",
                         [(['2020-05-12', CC050, CI050], [['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2]]),
                          (['2020-05-12', [], []], []),
                          (['2020-05-12', [], []], [])]
                         )
def test_find_yesterday_cc_entries(test_input1, expected):
    compare_obj = MarginChecker(test_input1[0], test_input1[1], test_input1[2])
    entries = compare_obj.find_yesterday_cc_entries()
    assert entries == expected


@pytest.mark.parametrize("test_input1, expected",
                         [(['2020-05-12', CC050, CI050], [['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2]]),
                          (['2020-05-12', [], []], [])])
def test_find_sod_ci_entries(test_input1, expected):
    compare_obj = MarginChecker(test_input1[0], test_input1[1], test_input1[2])
    entries = compare_obj.find_sod_ci_entries()
    assert entries == expected


@pytest.mark.parametrize("test_input1, expected",
                         [(['2020-05-12', CC050, CI050], [['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2]]),
                          (['2020-05-12', [], []], [])])
def test_find_eod_ci_entries(test_input1, expected):
    compare_obj = MarginChecker(test_input1[0], test_input1[1], test_input1[2])
    entries = compare_obj.find_eod_ci_entries()
    assert entries == expected


test_cc_with_sod_ci = {
    "expected_1": {'cc_with_sod_ci': {'report1': 'CC050_2020-05-11', 'report2': 'CI050_2020-05-12', 'missing': [[], []],
                                      'conflict': [[], []]}},
    "expected_2": {'cc_with_sod_ci': {'report1': 'CC050_2020-05-11', 'report2': 'CI050_2020-05-12', 'missing': [[], []],
                                      'conflict': [[], []]}},
    "expected_3": {
        'cc_with_sod_ci': {'report1': 'CC050_2020-05-11', 'report2': 'CI050_2020-05-12', 'missing': [[0], [0]],
                           'conflict': [[(0, 0)], [(0, 0)]]}}
}


@pytest.mark.parametrize("test_input1, expected", [(['2020-05-12', CC050, CI050], test_cc_with_sod_ci["expected_1"]),
                                                   (
                                                           ['2020-05-12', CC050_2, CI050_2],
                                                           test_cc_with_sod_ci["expected_2"]),
                                                   (['2020-05-12', CC050_3, CI050_3], test_cc_with_sod_ci["expected_3"])
                                                   ]
                         )
@patch.object(MarginChecker, 'compare_two_lol')
def test_cc_with_sod_ci(mock_compare_two_lol, test_input1, expected):
    compare_obj = MarginChecker(test_input1[0], test_input1[1], test_input1[2])
    mock_compare_two_lol.return_value = expected['cc_with_sod_ci']
    actual = compare_obj.cc_with_sod_ci()

    assert actual == expected


test_cc_with_eod_ci = {"expected_1": {'cc_with_eod_ci': {'report1': 'CC050_2020-05-11', 'report2': 'CI050_2020-05-11',
                                                         'missing': [[], []], 'conflict': [[], []]}},
                       "expected_2": {'cc_with_eod_ci': {'report1': 'CC050_2020-05-11', 'report2': 'CI050_2020-05-11',
                                                         'missing': [[], []], 'conflict': [[], []]}},
                       "expected_3": {'cc_with_eod_ci': {'report1': 'CC050_2020-05-11', 'report2': 'CI050_2020-05-11',
                                                         'missing': [[0], [0]], 'conflict': [[(0, 0)], [(0, 0)]]}}
                       }


@pytest.mark.parametrize("test_input1, expected", [(['2020-05-12', CC050, CI050], test_cc_with_eod_ci["expected_1"]),
                                                   (
                                                           ['2020-05-12', CC050_2, CI050_2],
                                                           test_cc_with_eod_ci["expected_2"]),
                                                   (['2020-05-12', CC050_3, CI050_3], test_cc_with_eod_ci["expected_3"])
                                                   ]
                         )
@patch.object(MarginChecker, 'compare_two_lol')
def test_cc_with_eod_ci(mock_compare_two_lol, test_input1, expected):
    compare_obj = MarginChecker(test_input1[0], test_input1[1], test_input1[2])
    mock_compare_two_lol.return_value = expected['cc_with_eod_ci']
    actual = compare_obj.cc_with_eod_ci()

    assert actual == expected


test_eod_with_sod = {"expected_1": {'ci_eod_with_sod': {'report1': 'CI050_2020-05-11', 'report2': 'CI050_2020-05-12',
                                                        'missing': [[], []], 'conflict': [[], []]}},
                     "expected_2": {'ci_eod_with_sod': {'report1': 'CI050_2020-05-11', 'report2': 'CI050_2020-05-12',
                                                        'missing': [[], []], 'conflict': [[], []]}},
                     "expected_3": {'ci_eod_with_sod': {'report1': 'CI050_2020-05-11', 'report2': 'CI050_2020-05-12',
                                                        'missing': [[0], [0]], 'conflict': [[(0, 0)], [(0, 0)]]}}
                     }


@pytest.mark.parametrize("test_input1, expected", [(['2020-05-12', CC050, CI050], test_eod_with_sod["expected_1"]),
                                                   (
                                                           ['2020-05-12', CC050_2, CI050_2],
                                                           test_eod_with_sod["expected_2"]),
                                                   (['2020-05-12', CC050_3, CI050_3], test_eod_with_sod["expected_3"])
                                                   ]
                         )
@patch.object(MarginChecker, 'compare_two_lol')
def test_cc_with_eod_ci(mock_compare_two_lol, test_input1, expected):
    compare_obj = MarginChecker(test_input1[0], test_input1[1], test_input1[2])
    mock_compare_two_lol.return_value = expected['ci_eod_with_sod']
    actual = compare_obj.ci_eod_with_sod()

    assert actual == expected
