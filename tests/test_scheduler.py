import unittest
from datetime import datetime, timedelta

from vsvs_scheduler.schedule import Schedule

from vsvs_scheduler.classroom import Classroom
from tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, converted_schedule, \
    partner_1_schedule, partner_2_schedule, partners_combined_schedule, partner_3_schedule, schedule_can_make_class
from vsvs_scheduler.volunteer import Volunteer


class ClassroomTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_class = Classroom(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                   group_number=0, school="Sunset Elementary", start_time="9:10:00 AM",
                                   end_time="10:25:00 AM")

    def test_free_time_duration(self):
        self.assertEqual(self.fake_class.free_time_duration(), timedelta(minutes=105))

    def test_assign_volunteer(self):
        fake_volunteer = Volunteer(name="Jane Doe", phone="000-000-000", email="jane.doe@vanderbilt.edu",
                                   leader_app=True, imported_schedule=sample_raw_schedule)
        fake_volunteer.availability = schedule_can_make_class
        self.fake_class.assign_volunteer(fake_volunteer)
        self.assertEqual(self.fake_class.num_of_volunteers, 1)
        self.assertEqual(fake_volunteer.group_number, 0)
        self.assertTrue(self.fake_class.team_leader)
        self.assertTrue(fake_volunteer.assigned_leader)


class VolunteerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_volunteer = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                       leader_app=True, imported_schedule=sample_raw_schedule)

    def test_convert_raw_scheduler_to_dict(self):
        schedule_dict = self.fake_volunteer.convert_raw_schedule_to_dict(sample_raw_schedule)
        self.assertEqual(schedule_dict, converted_schedule)
    def test_create_availability_schedule(self):
        free_time = self.fake_volunteer.create_availability_schedule(sample_raw_schedule)
        self.assertEqual(free_time, free_time_schedule)

    def test_day_availability(self):

    def test_can_make_classroom(self):


class PartnersTestCase(unittest.TestCase):
    def test_create_free_time_schedule(self):
        # create 3 dummy Volunteer objects for testing
        fake_partner_1 = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)
        fake_partner_2 = Volunteer(name="Bob Doe", phone="000-000-000", email="bob.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)
        fake_partner_3 = Volunteer(name="Charles Doe", phone="000-000-000", email="charles.doe@vanderbilt.edu",
                                   team_leader_app=True, imported_schedule=sample_raw_schedule)

        # Add 3 dummy schedules to each volunteer for testing
        fake_partner_1.availability = partner_1_schedule
        fake_partner_2.availability = partner_2_schedule
        fake_partner_3.availability = partner_3_schedule

        # Create a partner object and test that the create_partner_schedule returns the correct output
        partners = Partners([fake_partner_1, fake_partner_2, fake_partner_3])
        self.assertEqual(partners.create_availability_schedule(), partners_combined_schedule)


class SchedulerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Schedule(volunteer_file='../data/individuals.csv',
                                 classroom_file='../data/classrooms.csv', partner_file='../data/partners.csv')

    def test_data_import(self):
        self.assertEqual(len(self.scheduler.volunteer_list), 360)
        self.assertEqual(len(self.scheduler.partner_groups), 36)
        self.assertEqual(len(self.scheduler.classroom_list), 79)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError, msg="Sorry, the file volunteer_fake does not exist."):
            error_scheduler = Schedule(volunteer_file='volunteer_fake', classroom_file='../data/classrooms.csv',
                                       partner_file='../data/partners.csv')

        with self.assertRaises(FileNotFoundError, msg="Sorry, the file classroom_fake does not exist."):
            error_scheduler = Schedule(volunteer_file='../data/individuals.csv', classroom_file='classroom_fake',
                                       partner_file='../data/partners.csv')

        with self.assertRaises(FileNotFoundError, msg="Sorry, the file partners_fake does not exist."):
            error_scheduler = Schedule(volunteer_file='../data/individuals.csv',
                                       classroom_file='../data/classrooms.csv', partner_file='partners_fake')


if __name__ == '__main__':
    unittest.main()
