import unittest

from src import convert_schedule
from src.global_attributes import SCHOOL_TRAVEL_TIME


class TestConvertSchedule(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_convert_to_military(self):
        self.assertEqual(convert_schedule.convert_to_military('12:00 PM'), 1200)
        self.assertEqual(convert_schedule.convert_to_military('1:10 PM'), 1310)

    def test_calculate_free_time_needed(self):
        self.assertEqual(convert_schedule.calculate_free_time_needed(1200, 1300, SCHOOL_TRAVEL_TIME),
                         60 + 2 * SCHOOL_TRAVEL_TIME)


if __name__ == '__main__':
    unittest.main()
