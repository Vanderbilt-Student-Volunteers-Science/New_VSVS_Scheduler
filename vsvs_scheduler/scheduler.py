import csv
import os
import warnings
from datetime import datetime, timedelta

from classroom import Classroom
from volunteer import Volunteer, Partners


def file_prompt(applicant_type: str):
    """ Helper function to verify the file specified by the user can be located.

    :param applicant_type: specify the applicant type - 'individuals', 'partners', or 'classrooms'
    :return: path to file
    """
    filename = input(f"Enter the file path to the {applicant_type} file:\n")

    if filename == "" or filename is None:
        filename = f'../data/{applicant_type}.csv'

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Sorry, the file \"{filename}\" could not be found.\n")

    print(f"\nImporting {applicant_type} ...")

    return filename


class Scheduler:
    def __init__(self, earliest: str = "7:15", latest: str = "15:30", max_team_size: int = 4):
        self.earliest_time = datetime.strptime(earliest, "%H:%M")
        self.latest_time = datetime.strptime(latest, "%H:%M")

        self.individuals: list[Volunteer] = []
        self.classrooms: list[Classroom] = []
        self.partners: list[Partners] = []

        self.incomplete_classrooms = []
        self.max_size = max_team_size

        self.import_volunteers()
        self.not_found = self.import_partners()
        self.import_classrooms()

    def create_assignments(self):
        unassigned_partners = self.assign_partners()
        self.assign_volunteers("board")
        self.assign_volunteers("leaders")
        self.assign_volunteers()

        missing_team_leaders = [classroom for classroom in self.classrooms if not classroom.team_leader]
        incomplete_group = [classroom for classroom in self.classrooms if len(classroom.volunteers) < 3]

        for classroom in incomplete_group:
            classroom.unassign_volunteers()
        self.assign_volunteers()

        if missing_team_leaders:
            warnings.warn(f'WARNING: Classrooms are missing team leaders: {missing_team_leaders}')
        if incomplete_group:
            warnings.warn(f'WARNING: Classrooms without necessary number of volunteers {incomplete_group}')
        return {"unassigned": unassigned_partners, "not found": self.not_found}

    def assign_partners(self):
        """
        Assigns a group of partners to a classroom they all can make (if there is one) using partner1.partner_schedule.
        When a group is assigned, uses classroom.assign_volunteer() for each partner (including partner1).

        :return:
        """
        self.possible_classrooms()
        idx = 0
        unassigned_groups = []
        for group in self.partners:
            while group.group_number == -1 and idx < len(self.classrooms):
                curr_class = self.classrooms[idx]
                if group.can_make_class(curr_class) and self.max_size - len(curr_class.volunteers) >= len(
                        group.members):
                    group.assign_partners(curr_class)
                else:
                    idx += 1
            if group.group_number == -1:
                unassigned_groups.append(group)
        return unassigned_groups

    def assign_volunteers(self, volunteer_type: str = "default"):
        self.incomplete_classrooms = [classroom for classroom in self.classrooms if
                                      len(classroom.volunteers) < self.max_size]
        volunteer_list = self.individuals

        if volunteer_type == "leaders":
            volunteer_list = \
                [volunteer for volunteer in self.individuals if volunteer.group_number == -1 and volunteer.leader_app]
        elif volunteer_type == "board":
            volunteer_list = \
                [volunteer for volunteer in self.individuals if volunteer.group_number == -1 and volunteer.board]

        volunteer_list.sort(key=lambda volunteer: volunteer.possible_classrooms)

        for classroom in self.incomplete_classrooms:
            classroom.possible_volunteers = 0
            for volunteer in volunteer_list:
                if volunteer.can_make_class(classroom):
                    classroom.possible_volunteers += 1

        self.incomplete_classrooms.sort(key=lambda classroom: classroom.possible_volunteers)

        for volunteer in volunteer_list:
            idx = 0
            while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                classroom = self.incomplete_classrooms[idx]
                if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                    classroom.assign_volunteer(volunteer)
                    if len(classroom.volunteers) >= self.max_size:
                        self.incomplete_classrooms.remove(classroom)
                else:
                    idx += 1
        self.incomplete_classrooms.sort(key=lambda classroom: len(classroom.volunteers))

    def possible_classrooms(self):
        for volunteer in self.individuals:
            volunteer.possible_classrooms = 0
            for classroom in self.classrooms:
                if volunteer.group_number == -1 and volunteer.can_make_class(classroom):
                    volunteer.possible_classrooms += 1
        self.individuals.sort(key=lambda person: person.possible_classrooms)

        for classroom in self.classrooms:
            classroom.possible_volunteers = 0
            for volunteer in self.individuals:
                if volunteer.group_number == -1 and volunteer.can_make_class(classroom):
                    classroom.possible_volunteers += 1
        self.classrooms.sort(key=lambda group: group.possible_volunteers)

        for group in self.partners:
            for classroom in self.classrooms:
                if group.can_make_class(classroom):
                    group.increment_possible_classrooms()
        self.partners.sort(key=lambda person: person.possible_classrooms)

    def import_volunteers(self):
        """
        Imports volunteers' info from csv file and creates Volunteer instances.
        """
        filename = file_prompt("individuals")

        # opens file as individuals_csv and maps info in each row to a dict whose keys are given by the 1st row of
        # the csv
        with open(filename) as individuals_csv:
            csv_reader = csv.DictReader(individuals_csv)

            # pull data from row in the csv, create a Volunteer object, and add it to volunteers
            for row in csv_reader:
                schedule = list(row.values())[16:50]
                after_school = (lambda x: [] if x == "" else x.split(', '))(row["After-school"])
                volunteer = Volunteer(
                    first=row['First Name'].strip().lower().capitalize(),
                    last=row['Last Name'].strip().lower().capitalize(),
                    phone=row['Phone Number'],
                    email=row['Email Address'].strip(),
                    leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
                    imported_schedule=schedule,
                    after_school=(lambda x: [] if x == "" else x.split(', '))(row["After-school"]),
                    board_member=(lambda x: True if x == 'Yes' else False)(row['Board Member'])
                )
                self.individuals.append(volunteer)

            print('There are {} volunteers.\n'.format(len(self.individuals)))

    def import_classrooms(self):
        """
        Imports teacher and class info from csv file and create Classroom instances.
        """
        filename = file_prompt("classrooms")

        # opens file as classrooms_csv and maps info in each row to a dict whose keys are given by the 1st row of the
        # csv
        with open(filename) as classrooms_csv:
            csv_reader = csv.DictReader(classrooms_csv)
            group_num = 0

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
                        end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                        weekday=row[f'Days (Class {class_num} of {number_of_classes})']
                    )
                    self.classrooms.append(classroom)

            print('There are {} classrooms.\n'.format(len(self.classrooms)))

    def import_partners(self):
        """
        Imports partners' info from csv file and creates Partners instances.
        """
        filename = file_prompt("partners")

        partners_not_found = []

        # opens file as partners_csv and maps info in each row to a dict whose keys are given by the 1st row of the csv
        with open(filename) as partners_csv:
            csv_reader = csv.DictReader(partners_csv)

            # pull data from row in the csv, create a Partners object, and add it to partners
            for row in csv_reader:
                number_of_partners = int(row['Number of Partners'])
                partner_emails = [row['Email Address'].lower()]

                # for each person in the partners_csv row, add their email to partner_emails
                for i in range(1, number_of_partners):  # for each partner in the group
                    partner_email = row[f'Group Member #{i + 1}'].lower()
                    partner_emails.append(partner_email)

                # list comprehension adds all the partners' volunteer objects to the list 'group'
                group = [volunteer for volunteer in self.individuals if (volunteer.email in partner_emails)]

                # Remove duplicates
                for partner in group:
                    for partnered in self.partners:
                        if partner in partnered.members and len(group) > 1:
                            print(f'{partner.email} was in 2 groups. One deleted.')
                            self.partners.remove(partnered)

                if len(group) > 1:
                    self.partners.append(Partners(group))

                if len(group) < number_of_partners:
                    partners_not_found.append(partner_emails)

            # warnings.warn(f'WARNING: Not all group members were found: {partners_not_found}')
            print('There are {} partners.\n'.format(len(self.partners)))
            return partners_not_found

