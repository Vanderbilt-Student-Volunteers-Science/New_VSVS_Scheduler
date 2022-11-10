import unittest
from src.tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule

from src.scheduler import Scheduler


class SorterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(volunteer_file='../../data/individuals.csv',
                                  classroom_file='../../data/classrooms.csv', partner_file='../../data/partners.csv')

    def test_data_import(self):
        self.assertEqual(len(self.scheduler.volunteer_list), 360)
        self.assertEqual(len(self.scheduler.unassigned_volunteers), 360)
        self.assertEqual(len(self.scheduler.partner_groups), 36)
        self.assertEqual(len(self.scheduler.classroom_list), 79)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError, msg="Sorry, the file volunteer_fake does not exist."):
            error_scheduler = Scheduler(volunteer_file='volunteer_fake', classroom_file='../../data/classrooms.csv',
                                        partner_file='../../data/partners.csv')

        with self.assertRaises(FileNotFoundError, msg="Sorry, the file classroom_fake does not exist."):
            error_scheduler = Scheduler(volunteer_file='../../data/individuals.csv', classroom_file='classroom_fake',
                                        partner_file='../../data/partners.csv')

        with self.assertRaises(FileNotFoundError, msg="Sorry, the file partners_fake does not exist."):
            error_scheduler = Scheduler(volunteer_file='../../data/individuals.csv',
                                        classroom_file='../../data/classrooms.csv', partner_file='partners_fake')


if __name__ == '__main__':
    unittest.main()
