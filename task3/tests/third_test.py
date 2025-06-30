import unittest

from task3 import appearance


class TestAppearance(unittest.TestCase):
    def test_basic_case(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [50, 150, 180, 250],
            'tutor': [80, 120, 160, 220]
        }
        self.assertEqual(appearance(intervals), 40)

    def test_no_overlap(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [50, 90, 210, 250],
            'tutor': [80, 99, 201, 220]
        }
        self.assertEqual(appearance(intervals), 0)

    def test_multiple_intervals(self):
        intervals = {
            'lesson': [100, 500],
            'pupil': [50, 150, 200, 300, 400, 550],
            'tutor': [120, 180, 250, 350, 450, 600]
        }
        self.assertEqual(appearance(intervals), 130)

    def test_edge_cases(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [100, 150, 150, 200],
            'tutor': [100, 200]
        }
        self.assertEqual(appearance(intervals), 100)

    def test_completely_inside(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [120, 180],
            'tutor': [110, 190]
        }
        self.assertEqual(appearance(intervals), 60)

    def test_partial_overlap(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [80, 150],
            'tutor': [150, 250]
        }
        self.assertEqual(appearance(intervals), 0)

    def test_original_test_cases(self):
        tests = [
            {'intervals': {'lesson': [1594663200, 1594666800],
                           'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                           'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
             'answer': 3117},
            {'intervals': {'lesson': [1594702800, 1594706400],
                           'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                                     1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                                     1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                                     1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                                     1594706524, 1594706524, 1594706579, 1594706641],
                           'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
             'answer': 3577},
            {'intervals': {'lesson': [1594692000, 1594695600],
                           'pupil': [1594692033, 1594696347],
                           'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
             'answer': 3565}
        ]

        for test in tests:
            result = appearance(test['intervals'])
            self.assertEqual(result, test['answer'])

    def test_empty_intervals(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [],
            'tutor': [150, 180]
        }
        self.assertEqual(appearance(intervals), 0)


if __name__ == '__main__':
    unittest.main()
