import unittest
from src.applicant import Volunteer
from src.tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule


class VolunteerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_volunteer = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                       team_leader_app=True, index=0, imported_schedule=sample_raw_schedule)

    def test_schedule_conversions(self):
        schedule_dict = self.fake_volunteer.convert_imported_list_to_schedule_dict(sample_raw_schedule)
        self.assertEqual(schedule_dict, converted_schedule)
        free_time = self.fake_volunteer.schedule_to_free_time(sample_raw_schedule)
        self.assertEqual(free_time, free_time_schedule)


if __name__ == '__main__':
    unittest.main()
