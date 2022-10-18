import unittest
from src.tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule

from src.sorter import Sorter


class SorterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sorter = Sorter(max_team_size=5, min_team_size=3, travel_time=15)

    def test_volunteer_import(self):
        self.sorter.import_volunteers('test_data/individuals.csv')
        self.assertEqual(len(self.sorter.volunteer_list), 360)

    def test_classroom_import(self):
        self.sorter.import_classrooms('test_data/classrooms.csv')
        self.assertEqual(len(self.sorter.classroom_list), 79)

    def test_convert_imported_list_to_free_time(self):
        self.assertEqual(self.sorter.schedule_to_free_time(sample_raw_schedule), free_time_schedule)


if __name__ == '__main__':
    unittest.main()
