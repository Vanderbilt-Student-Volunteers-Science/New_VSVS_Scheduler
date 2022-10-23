import unittest
from src.tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule

from src.scheduler import Scheduler


class SorterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(max_team_size=5, min_team_size=3, travel_time=15)

    def test_volunteer_and_partners_import(self):
        self.scheduler.import_volunteers('test_data/individuals.csv')
        self.scheduler.import_partners('test_data/partners.csv')
        self.assertEqual(len(self.scheduler.volunteer_list), 360)
        self.assertEqual(len(self.scheduler.partner_groups), 36)

    def test_classroom_import(self):
        self.scheduler.import_classrooms('test_data/classrooms.csv')
        self.assertEqual(len(self.scheduler.classroom_list), 79)

    def test_schedule_to_free_time(self):
        self.assertEqual(self.scheduler.schedule_to_free_time(sample_raw_schedule), free_time_schedule)

    def test_convert_imported_list_to_schedule(self):
        self.assertEqual(self.scheduler.convert_imported_list_to_schedule(sample_raw_schedule), converted_schedule)


if __name__ == '__main__':
    unittest.main()
