"""
Mock input module based on assumption that the source data would be a LOL (List of Lists)
"""
CC050 = [

    # [date, clearing member, account, margin type, margin]
    # end-of-day report of 2020-05-11 in CC050 table
    ['2020-05-11', 'Bank 1', 'A1', 'SPAN', 3212.2],
    ['2020-05-11', 'Bank 1', 'A1', 'IMSM', 837.1],

    ['2020-05-11', 'Bank 1', 'A2', 'SPAN', 8963.3],
    ['2020-05-11', 'Bank 1', 'A2', 'IMSM', 76687.9],

    ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 821.4],
    ['2020-05-11', 'Bank 2', 'A1', 'SPAN', 8766.4],

]

CI050 = [
    # [date, time of day, clearing member, account, margin type, margin]
    ['2020-05-11', '18:00:00', 'Bank 1', 'A1', 'SPAN', 2882.2],
    ['2020-05-11', '18:00:00', 'Bank 1', 'A1', 'IMSM', 988.1],

    ['2020-05-11', '18:00:00', 'Bank 1', 'A2', 'SPAN', 788.3],
    ['2020-05-11', '18:00:00', 'Bank 1', 'A2', 'IMSM', 908.9],
    ['2020-05-11', '18:00:00', 'Bank 2', 'A1', 'SPAN', 123.4],
    ['2020-05-11', '18:00:00', 'Bank 2', 'A1', 'IMSM', 8326.4],
    # "last" intraday report of 2020-05-11 in CI050 table
    ['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
    ['2020-05-11', '19:00:00', 'Bank 1', 'A1', 'IMSM', 837.1],
    #changed this 76687.9 to 8963.4 to trigger mismatch
    ['2020-05-11', '19:00:00', 'Bank 1', 'A2', 'SPAN', 8963.4],
    #changed this 76687.9 to 76687.8 to trigger mismatch
    ['2020-05-11', '19:00:00', 'Bank 1', 'A2', 'IMSM', 76687.8],

    ['2020-05-11', '19:00:00', 'Bank 2', 'A1', 'SPAN', 821.4],
    ['2020-05-11', '19:00:00', 'Bank 2', 'A1', 'IMSM', 8766.4],
    # "first" intraday report of 2020-05-12 in CI050 table
    ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'SPAN', 3212.2],
    ['2020-05-12', '08:00:00', 'Bank 1', 'A1', 'IMSM', 837.1],
    ['2020-05-12', '08:00:00', 'Bank 1', 'A2', 'SPAN', 8963.3],
    ['2020-05-12', '08:00:00', 'Bank 1', 'A2', 'IMSM', 76687.9],
    ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'SPAN', 821.4],
    ['2020-05-12', '08:00:00', 'Bank 2', 'A1', 'IMSM', 8766.4],
    # "second" intraday report of 2020-05-12 in CI050 table
    ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'SPAN', 3133.9],
    ['2020-05-12', '09:00:00', 'Bank 1', 'A1', 'IMSM', 137.1],
    ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'SPAN', 2963.3],
    ['2020-05-12', '09:00:00', 'Bank 1', 'A2', 'IMSM', 74687.9],
    ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'SPAN', 811.4],
    ['2020-05-12', '09:00:00', 'Bank 2', 'A1', 'IMSM', 8366.4],
]
