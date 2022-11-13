import unittest
from src.scheduler import Scheduler

from src.applicant import Volunteer, Classroom
from src.partners import Partners
from src.tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule, \
    partner_1_schedule, partner_2_schedule, partners_combined_schedule, partner_3_schedule, schedule_can_make_class


class ClassroomTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_class = Classroom(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                   group_number=0, school="Sunset Elementary", start_time="9:10:00 AM",
                                   end_time="10:25:00 AM")

    def test_free_time_duration(self):
        self.assertEqual(self.fake_class.free_time_duration(), 105)

    def test_can_make_class(self):
        always_unavailable = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}}
        self.assertTrue(self.fake_class.can_make_class(schedule_can_make_class))
        self.assertFalse(self.fake_class.can_make_class(always_unavailable))

    def test_assign_volunteer(self):
        fake_volunteer = Volunteer(name="Jane Doe", phone="000-000-000", email="jane.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)
        fake_volunteer.free_time = schedule_can_make_class
        self.fake_class.assign_volunteer(fake_volunteer)
        self.assertEqual(self.fake_class.num_of_volunteers, 1)
        self.assertEqual(fake_volunteer.group_number, 0)
        self.assertTrue(self.fake_class.team_leader)
        self.assertTrue(fake_volunteer.leader)


class VolunteerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_volunteer = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                       team_leader_app=True, imported_schedule=sample_raw_schedule)

    def test_schedule_conversions(self):
        schedule_dict = self.fake_volunteer.convert_imported_list_to_schedule_dict(sample_raw_schedule)
        free_time = self.fake_volunteer.schedule_to_free_time(sample_raw_schedule)
        self.assertEqual(schedule_dict, converted_schedule)
        self.assertEqual(free_time, free_time_schedule)


class PartnersTestCase(unittest.TestCase):
    def test_create_partner_schedule(self):
        # create 3 dummy Volunteer objects for testing
        fake_partner_1 = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)
        fake_partner_2 = Volunteer(name="Bob Doe", phone="000-000-000", email="bob.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)
        fake_partner_3 = Volunteer(name="Charles Doe", phone="000-000-000", email="charles.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)

        # Add 3 dummy schedules to each volunteer for testing
        fake_partner_1.free_time = partner_1_schedule
        fake_partner_2.free_time = partner_2_schedule
        fake_partner_3.free_time = partner_3_schedule

        # Create a partner object and test that the create_partner_schedule returns the correct output
        partners = Partners([fake_partner_1, fake_partner_2, fake_partner_3])
        self.assertEqual(partners.create_partner_schedule(), partners_combined_schedule)


class SchedulerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler(volunteer_file='../../data/individuals.csv',
                                  classroom_file='../../data/classrooms.csv', partner_file='../../data/partners.csv')

    def test_data_import(self):
        self.assertEqual(len(self.scheduler.volunteer_list), 360)
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
