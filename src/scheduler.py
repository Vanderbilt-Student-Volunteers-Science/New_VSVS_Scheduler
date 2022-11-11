import csv
from datetime import datetime, timedelta
from src.partners import Partners
from src.applicant import Volunteer, Classroom


# Helper functions for importing data from csv files
def import_volunteers(filename: str):
    """Reads csv with volunteer information and creates a Volunteer object from each row.

    :param filename: filepath to the csv with volunteer info
    :return:list of Volunteer objects
    """
    volunteers = []

    # Check that the file exists
    try:
        open(filename)
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + " does not exist."

    # opens file as individuals_csv and maps info in each row to a dict whose keys are given by the 1st row of the csv
    with open(filename) as individuals_csv:
        csv_reader = csv.DictReader(individuals_csv)
        volunteer_idx = 0

        # pull data from row in the csv, create a Volunteer object, and add it to volunteers
        for row in csv_reader:
            volunteer_idx += 1
            schedule = list(row.values())[16:50]
            volunteer = Volunteer(
                index=volunteer_idx,
                name=row['First Name'].strip() + ' ' + row['Last Name'].strip(),
                phone=row['Phone Number'],
                email=row['Email'].strip(),
                team_leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
                imported_schedule=schedule
            )
            volunteers.append(volunteer)
            print(str(volunteer) + f" {volunteer.free_time}")

    print('There are {} volunteers.'.format(len(volunteers)))
    return volunteers


def import_classrooms(filename: str):
    """Reads csv with classroom information and creates a Classroom object from each row.

    :param filename: filepath to the csv with volunteer info
    :return: list of Classroom objects
    """
    classrooms = []

    # Check that the file exists
    try:
        open(filename)
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + "does not exist."

    # opens file as classrooms_csv and maps info in each row to a dict whose keys are given by the 1st row of the csv
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
                classroom = Classroom(group_number=group_num,
                                      name=teacher_name,
                                      phone=teacher_phone,
                                      school=school,
                                      email=email,
                                      start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                                      end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                                      )
                classrooms.append(classroom)
        print('There are {} classrooms.'.format(len(classrooms)))
        return classrooms


class Scheduler:

    def __init__(self, volunteer_file: str, partner_file: str, classroom_file: str, max_team_size: int = 4,
                 min_team_size: int = 3):

        # Import data
        self.volunteer_list = import_volunteers(volunteer_file)
        self.classroom_list = import_classrooms(classroom_file)
        self.partner_groups = self.import_partners(partner_file)

        self.max_team_size = max_team_size
        self.min_team_size = min_team_size

        self.sort_by_availability()
        self.find_class_for_partners()
        self.assign_team_leaders()
        self.assign_volunteers()
        self.assign_second_time()

    def import_partners(self, filename: str):
        """Reads csv with partner group information and creates a Partners object from each row.

        :param filename: filepath to the csv with volunteer info
        :return: list of Partners objects
        """
        partners = []

        # Check that the file exists
        try:
            open(filename)
        except FileNotFoundError:
            msg = "Sorry, the file " + filename + "does not exist."

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
                group = [volunteer for volunteer in self.volunteer_list if volunteer.email in partner_emails]
                if len(group) < number_of_partners:
                    print(f'WARNING: Not all group members were found: {partner_emails}')
                if len(group) > 1:
                    partners_group = Partners(group)
                    partners.append(partners_group)
        return partners

    def sort_by_availability(self):
        """Sorts volunteer and partner lists from the least to the greatest number of classrooms possible."""

        # Counts how many classrooms each partner group can make
        for partners in self.partner_groups:
            for classroom in self.classroom_list:
                if classroom.can_make_class(partners.free_time):
                    partners.classrooms_possible += 1

        # Counts how many classrooms each volunteer can make
        for person in self.volunteer_list:
            for classroom in self.classroom_list:
                if classroom.can_make_class(person.free_time):
                    person.classrooms_possible += 1

        # Sorts the volunteer_list and partners_list from the least to the greatest number of classrooms possible
        self.volunteer_list.sort(key=lambda volunteer: volunteer.classrooms_possible)
        self.partner_groups.sort(key=lambda group: group.classrooms_possible)

    def sort_classrooms_by_num_of_volunteers(self):
        """Sorts the classroom_list from least to greatest number of volunteers assigned."""
        self.classroom_list.sort(key=lambda classroom: classroom.num_of_volunteers, reverse=True)

    def assign_volunteers(self):
        """Assigns all unassigned volunteers to classroom groups. Prioritizes assigning each volunteer to a partially-filled
          classroom group over an empty classroom group.

          """
        for volunteer in self.volunteer_list:
            self.sort_classrooms_by_num_of_volunteers()
            classroom_idx = 0
            while volunteer.group_number == -1 and classroom_idx < len(self.classroom_list):
                classroom = self.classroom_list[classroom_idx]
                if classroom.can_make_class(volunteer.free_time) and classroom.num_of_volunteers < self.max_team_size:
                    classroom.assign_volunteer(volunteer)
                else:
                    classroom_idx += 1

    def assign_second_time(self):
        """Unassigns all volunteers from a classroom

                :return: list of the volunteers that were unassigned
                """
        self.sort_classrooms_by_num_of_volunteers()
        for classroom in self.classroom_list:
            if classroom.num_of_volunteers < self.min_team_size:
                group_num = classroom.group_number
                for volunteer in self.volunteer_list:
                    if volunteer.group_number == group_num:
                        volunteer.set_group_number(-1)
                        volunteer.assigned_t_leader = False
                        classroom.number_of_volunteers = 0
                        classroom.team_leader = False
        self.assign_volunteers()

    def find_class_for_partners(self):
        """
        Assigns partners to a classroom they all can make based on parnters.free_time. When classroom is found,
        classroom.assign_partners is used to assign them.

        :return:
        """
        self.sort_classrooms_by_num_of_volunteers()
        for partners in self.partner_groups:
            class_idx = 0
            while partners.group_number == -1 and class_idx < len(self.classroom_list):
                curr_class = self.classroom_list[class_idx]
                if curr_class.can_make_class(partners.free_time) & (self.max_team_size - curr_class.num_of_volunteers):
                    curr_class.assign_partners(partners)
                else:
                    class_idx += 1
            if partners.group_number == -1:
                print(f"WARNING:{str(partners)} partner group could not be assigned together because of "
                      "scheduling conflicts.")
        self.sort_by_availability()

    def assign_team_leaders(self):
        """Assigns team leaders to classroom groups that don't have them. Prioritizes assigning team leaders to
        partially-filled classroom groups over empty classroom groups.

        :return:
        """
        self.sort_classrooms_by_num_of_volunteers()
        for volunteer in self.volunteer_list:
            if volunteer.leader_app:
                class_idx = 0
                while volunteer.group_number == -1 and class_idx < len(self.classroom_list):
                    curr_class = self.classroom_list[class_idx]
                    if curr_class.can_make_class(volunteer.free_time, ) \
                            and self.max_team_size - curr_class.num_of_volunteers and not curr_class.team_leader:
                        curr_class.assign_volunteer(volunteer)
                    else:
                        class_idx += 1
