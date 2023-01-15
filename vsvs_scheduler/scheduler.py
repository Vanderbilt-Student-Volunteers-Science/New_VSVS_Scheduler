import csv
import os
import warnings
from datetime import datetime

from src import MAX_TEAM_SIZE
from src.classroom import Classroom
from src.volunteer import Volunteer, Partners


def file_prompt(applicant_type: str):
    applications = input(f"Enter the file path to the {applicant_type} file:\n")
    if not os.path.isfile(applications):
        raise FileNotFoundError(f"Sorry, the file \"{applications}\" could not be found.\n")


class Scheduler:
    def __init__(self, earliest: str = "7:15", latest: str = "15:30"):
        earliest_time = datetime.strptime(earliest, "%H:%M")
        latest_time = datetime.strptime(latest, "%H:%M")
        self.individuals = []
        self.classrooms = []
        self.incomplete_classrooms = []
        self.partners = []

    def import_volunteers(self):
        """ reads csv with volunteer information and creates a Volunteer object from each row
        :param filename: filepath to the csv with volunteer info
        """
        filename = file_prompt("individuals")
        print("Importing Volunteers ...\n")

        # opens file as individuals_csv and maps info in each row to a dict whose keys are given by the 1st row of
        # the csv
        with open(filename) as individuals_csv:
            csv_reader = csv.DictReader(individuals_csv)

            # pull data from row in the csv, create a Volunteer object, and add it to volunteers
            for row in csv_reader:
                schedule = list(row.values())[16:50]
                volunteer = Volunteer(
                    name=row['First Name'].strip().lower().capitalize() + ' ' + row[
                        'Last Name'].strip().lower().capitalize(),
                    phone=row['Phone Number'],
                    email=row['Email'].strip(),
                    leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
                    imported_schedule=schedule
                )
            self.individuals.append(volunteer)

            print('There are {} volunteers.'.format(len(self.individuals)))

    def import_classrooms(self):
        """Reads csv with classroom information and creates a Classroom object from each row.
        :param filename: filepath to the csv with volunteer info
        """
        filename = file_prompt("classrooms")
        print("Importing Classrooms ... \n")

        # opens file as classrooms_csv and maps info in each row to a dict whose keys are given by the 1st row of the
        # csv
        with open(filename) as classrooms_csv:
            csv_reader = csv.DictReader(classrooms_csv)
            group_num = 1

            # pull data from row in the csv
            for row in csv_reader:  # for each teacher
                teacher_name = row['Name']
                teacher_phone = row['Cell Phone Number']
                school = row['School']
                email = row['Email Address']
                number_of_classes = row['Number of Classes']

                # for each of the teachers classes a Classroom object is created and added to classrooms
                for i in range(int(number_of_classes)):
                    group_num += 1
                    class_num = i + 1  # class_num keeps track of which class out of the total being created
                    classroom = Classroom(
                        group_number=group_num,
                        name=teacher_name,
                        phone=teacher_phone,
                        school=school,
                        email=email,
                        start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                        end_time=row[f'End Time (Class {class_num} of {number_of_classes})']
                    )
                    self.classrooms.append(classroom)
                print('There are {} classrooms.'.format(len(self.classrooms)))

    def import_partners(self):
        """

        :param file_name:
        :return:
        """
        filename = file_prompt("partners")
        print("Importing Partners ...\n")

        # opens file as partners_csv and maps info in each row to a dict whose keys are given by the 1st row of the csv
        with open(filename) as partners_csv:
            csv_reader = csv.DictReader(partners_csv)

            # pull data from row in the csv, create a Partners object, and add it to partners
            for row in csv_reader:
                number_of_partners = int(row['Number of Partners'])
                partner_emails = []

                # for each person in the partners_csv row, add their email to partner_emails
                for i in range(number_of_partners):  # for each partner in the group
                    partner_email = row[f'Group Member #{i + 1}'].lower()
                    partner_emails.append(partner_email)

                # list comprehension adds all the partners' volunteer objects to the list 'group'
                group = [volunteer for volunteer in self.individuals if volunteer.email in partner_emails]
                if len(group) < number_of_partners:
                    warnings.warn(f'WARNING: Not all group members were found: {partner_emails}')
                if len(group) > 1:
                    self.partners.append(Partners(group))

            print('There are {} partners.'.format(len(self.partners)))

    def assign_partners(self):
        """
        Assigns a group of partners to a classroom they all can make (if there is one) using partner1.partner_schedule.
        When a group is assigned, uses classroom.assign_volunteer() for each partner (including partner1).


        :param partner1:the Volunteer object of the first partner in the group; the Volunteer object that contains the
                        information of the group of partners (only one is set when partners.csv is imported)
        :return:
        """
        idx = 0

        for group in self.partners:
            while group.group_number == -1 and idx < len(self.classrooms):
                curr_class = self.classrooms[idx]
                if group.can_make_class(curr_class) and MAX_TEAM_SIZE - curr_class.volunteers_assigned >= len(
                        group.members):
                    group.assign_partners(curr_class)
                else:
                    idx += 1
            if group.group_number == -1:
                print(
                    "WARNING: " + group.email + "'s partner group could not be assigned together because of scheduling" +
                    "conflicts.")

    def assign_leaders(self):
        self.incomplete_classrooms = [classroom for classroom in self.classrooms if
                                      classroom.volunteers_assigned < MAX_TEAM_SIZE]
        team_leader_apps = \
            [volunteer for volunteer in self.individuals if volunteer.group_number == -1 and volunteer.leader_app]

        team_leader_apps.sort(key=lambda volunteer: volunteer.possible_classrooms)

        for volunteer in team_leader_apps:
            idx = 0
            while volunteer.group_number == -1 and idx < len(self.classrooms):
                classroom = self.classrooms[idx]
                if volunteer.can_make_class(classroom) and not classroom.team_leader:
                    classroom.assign_volunteer(volunteer)
                    if classroom.volunteers_assigned >= MAX_TEAM_SIZE:
                        self.incomplete_classrooms.remove(classroom)
                else:
                    idx += 1

    def assign_volunteers(self):
        for volunteer in self.individuals:
            idx = 0
            while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                classroom = self.incomplete_classrooms[idx]
                if volunteer.can_make_class(classroom):
                    classroom.assign_volunteer(volunteer)
                    if classroom.volunteers_assigned >= MAX_TEAM_SIZE:
                        self.incomplete_classrooms.remove(classroom)
                else:
                    idx += 1

    def possible_classrooms(self):
        for volunteer in self.individuals:
            if volunteer.group_number == -1:
                for classroom in self.classrooms:
                    if volunteer.can_make_class(classroom):
                        volunteer.possible_classrooms += 1
        self.individuals = self.individuals.sort(key=lambda person: person.possible_classrooms)

        for group in self.partners:
            for classroom in self.classrooms:
                if group.can_make_class(classroom):
                    group.increment_possible_classrooms()
        self.partners = self.partners.sort(key=lambda person: person.possible_classrooms)
