import unittest
from unittest.mock import patch

from vsvs_scheduler.classroom import Classroom
from tests.test_data.sample_data_and_outputs import sample_raw_schedule, free_time_schedule, schedule_dict_from_raw, \
    partner_1_schedule, partner_2_schedule, partner_3_schedule, schedule_can_make_class, \
    sample_Monday_availability
from vsvs_scheduler.scheduler import Scheduler
from vsvs_scheduler.volunteer import Volunteer, Partners

fake_volunteer1 = Volunteer(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                            leader_app=True, imported_schedule=sample_raw_schedule)

fake_volunteer2 = Volunteer(name="Bob Doe", phone="000-000-000", email="bob.doe@vanderbilt.edu",
                            leader_app=True, imported_schedule=sample_raw_schedule)

fake_volunteer3 = Volunteer(name="Charles Doe", phone="000-000-000", email="charles.doe@vanderbilt.edu",
                            leader_app=True, imported_schedule=sample_raw_schedule)

fake_classroom1 = Classroom(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                            group_number=0, school="Sunset Elementary", start_time="11:15:00 AM",
                            end_time="12:30:00 PM")

fake_classroom2 = Classroom(name="John Doe", phone="000-000-000", email="john.doe@vanderbilt.edu",
                            group_number=1, school="Sunset Elementary", start_time="12:00:00 PM",
                            end_time="12:30:00 PM", weekday="Tuesday")


class ClassroomTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_class = fake_classroom1

    def test_free_time_duration(self):
        self.assertEqual(self.fake_class.duration(), 105)

    def test_assign_volunteer(self):
        fake_volunteer = fake_volunteer1
        fake_volunteer.availability = schedule_can_make_class
        self.fake_class.assign_volunteer(fake_volunteer)
        self.assertEqual(len(self.fake_class.volunteers), 1)
        self.assertEqual(fake_volunteer.group_number, 0)
        self.assertTrue(self.fake_class.team_leader)
        self.assertTrue(fake_volunteer.assigned_leader)

    # fail to assign to class with too many members test


class VolunteerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_volunteer = fake_volunteer1

    def test_convert_raw_scheduler_to_dict(self):
        schedule_dict = self.fake_volunteer.convert_to_unavailability_dict(sample_raw_schedule)
        self.assertEqual(schedule_dict, schedule_dict)

    def test_day_availability(self):
        day_availability = self.fake_volunteer.find_day_availability(schedule_dict_from_raw["Monday"])
        self.assertEqual(day_availability, sample_Monday_availability)

    def test_can_make_classroom(self):
        self.assertTrue(self.fake_volunteer.can_make_class(fake_classroom1))
        self.assertFalse(self.fake_volunteer.can_make_class(fake_classroom2))

    def test_create_availability_schedule(self):
        free_time = self.fake_volunteer.create_availability_schedule(sample_raw_schedule)
        self.assertEqual(free_time, free_time_schedule)


class PartnersTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fake_volunteer1.availability = partner_1_schedule
        fake_volunteer2.availability = partner_2_schedule
        fake_volunteer3.availability = partner_3_schedule

        cls.partner_group = Partners([fake_volunteer1, fake_volunteer2, fake_volunteer3])

    def test_can_make_class(self):
        self.assertTrue(self.partner_group.can_make_class(fake_classroom2))

    def test_increment_possible_classrooms(self):
        pre_increment_possible_classrooms = self.partner_group.possible_classrooms
        self.partner_group.increment_possible_classrooms()
        self.assertEqual(self.partner_group.possible_classrooms, pre_increment_possible_classrooms + 1)
        self.assertTrue(fake_classroom2.team_leader)
        self.assertTrue(self.partner_group.members[0].assigned_leader)
        for member in self.partner_group.members:
            self.assertEqual(member.possible_classrooms, pre_increment_possible_classrooms + 1)

    def test_assign_partners(self):
        self.partner_group.assign_partners(fake_classroom2)
        self.assertEqual(self.partner_group.group_number, fake_classroom2.group_number)
        self.assertEqual(len(fake_classroom2.volunteers), len(self.partner_group.members))
        for member in self.partner_group.members:
            self.assertEqual(member.group_number, fake_classroom2.group_number)

    # fail to assign class with too many members test
    # test group that can't make it to class


class SchedulerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = Scheduler()

    def test_import_individual_functions(self):
        with patch('builtins.input', return_value='test_data/individuals.csv'):
            self.scheduler.import_volunteers()
            self.assertEqual(len(self.scheduler.individuals), 360)

        with patch('builtins.input', return_value='test_data/partners.csv'):
            self.scheduler.import_partners()
            self.assertEqual(len(self.scheduler.partners), 42)

        with patch('builtins.input', return_value='test_data/classrooms.csv'):
            self.scheduler.import_classrooms()
            self.assertEqual(len(self.scheduler.classrooms), 79)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError, msg="Sorry, the file volunteer_fake does not exist."):
            with patch('builtins.input', return_value='volunteer_fake'):
                self.scheduler.import_volunteers()




if __name__ == '__main__':
    unittest.main()
