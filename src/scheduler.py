import csv
from datetime import datetime, timedelta
from src.partners import Partners
from src.volunteer import Volunteer, Classroom


def can_make_class(schedule: dict, classroom: Classroom):
    """ Returns boolean of whether volunteer/partner group can make a classroom based on the schedule parameter

    :param schedule: free time schedule of a volunteer or partner group
    :param classroom: classroom that we are checking compatability with
    :return: bool: whether volunteer/partners can make that class
    """
    day = classroom.weekday
    time = classroom.start_time.strftime('%H:%M')
    if time in schedule[day]:
        return schedule[day][time] >= classroom.free_time_duration()
    else:
        return False


class Scheduler:

    def __init__(self, volunteer_file: str, partner_file: str, classroom_file: str, max_team_size: int = 4,
                 min_team_size: int = 3, travel_time: int = 15):
        """

        :param max_team_size:maximum number of volunteers to allow in a classroom group
        :param min_team_size:minimum acceptable number of volunteers in a classroom group that can visit a classroom
        :param travel_time:minutes to travel one-way to any school
        """
        self.volunteer_list = []
        self.unassigned_volunteers = []
        self.classroom_list = []
        self.partner_groups = []

        # Import data
        self.import_volunteers(volunteer_file)
        self.import_partners(partner_file)
        self.import_classrooms(classroom_file)

        self.max_team_size = max_team_size
        self.min_team_size = min_team_size
        self.travel_time = travel_time

        self.sort_by_availability()
        self.find_class_for_partners()

    def import_volunteers(self, filename: str):
        """reads csv with volunteer information and creates a Volunteer object from each row

        :param filename: filepath to the csv with volunteer info
        :return:
        """
        try:
            open(filename)
        except FileNotFoundError:
            msg = "Sorry, the file " + filename + " does not exist."

        with open(filename) as individuals_csv:  # opens file as individuals_csv
            # maps the information in each row to a dict whose keys are given by the first row in the csv
            csv_reader = csv.DictReader(individuals_csv)
            volunteer_idx = 0
            # pull data from row in the csv, create a Volunteer object, and add it to volunteer_list
            for row in csv_reader:  # for each individual
                volunteer_idx += 1
                schedule = list(row.values())[16:50]
                volunteer = Volunteer(
                    index=volunteer_idx,
                    name=row['First Name'].strip() + ' ' + row['Last Name'].strip(),
                    phone=row['Phone Number'],
                    email=row['Email'].strip(),
                    team_leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
                    free_time=schedule
                )
                self.volunteer_list.append(volunteer)
                self.unassigned_volunteers.append(volunteer)

        print('There are {} volunteers.'.format(len(self.volunteer_list)))
        return self.volunteer_list

    def import_classrooms(self, filename: str):
        """

        :param filename:
        :return:
        """
        try:
            open(filename)
        except FileNotFoundError:
            msg = "Sorry, the file " + filename + "does not exist."

        with open(filename) as classrooms_csv:  # opens classrooms.csv as classrooms_csv
            # maps the information in each row to a dict whose keys are given by the first row in the csv
            csv_reader = csv.DictReader(classrooms_csv)
            group_num = 1
            for row in csv_reader:  # for each teacher
                teacher_name = row['Name']
                teacher_phone = row['Cell Phone Number']
                school = row['School']
                email = row['Email Address']
                number_of_classes = row['Number of Classes']
                for i in range(int(number_of_classes)):  # for all of that teacher's classes
                    group_num += 1
                    class_num = i + 1  # class_num keeps track of which class out of the total being created
                    # creates a Classroom object and adds it to classroom_list attribute in the sorter class
                    classroom = Classroom(group_number=group_num,
                                          name=teacher_name,
                                          phone=teacher_phone,
                                          school=school,
                                          email=email,
                                          start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                                          end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                                          )
                    self.classroom_list.append(classroom)
            print('There are {} classrooms.'.format(len(self.classroom_list)))
            return self.classroom_list

    def import_partners(self, filename: str):
        """

        :param filename:
        :return:
        """

        try:
            open(filename)
        except FileNotFoundError:
            msg = "Sorry, the file " + filename + "does not exist."

        with open(filename) as partners_csv:  # opens partners.csv as partners_csv
            # returns the information in each row as a dictionary whose keys are given by the first row in the csv
            csv_reader = csv.DictReader(partners_csv)
            for row in csv_reader:  # for each group of partners
                number_of_partners = int(row['Number of Partners'])  # number of partners in the group
                partner_emails = []  # list of the partner volunteer emails
                for i in range(number_of_partners):  # for each partner in the group
                    partner_email = row[f'Group Member #{i + 1}'].lower()
                    partner_emails.append(partner_email)  # add partner email to the list
                # add all the partners' volunteer objects to the list 'group'
                group = [volunteer for volunteer in self.volunteer_list if volunteer.email in partner_emails]
                if len(group) < number_of_partners:
                    print(f'WARNING: Not all group members were found: {partner_emails}')
                if len(group) > 1:
                    partners = Partners(group)
                    self.partner_groups.append(partners)
        return self.partner_groups

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
                if can_make_class(partners.free_time, curr_class) & (self.max_team_size - curr_class.num_of_volunteers):
                    self.assign_partners(partners, curr_class)
                else:
                    class_idx += 1
            if partners.group_number == -1:
                print(f"WARNING:{partners.volunteers} partner group could not be assigned together because of "
                      "scheduling conflicts.")

    def assign_partners(self, partners: Partners, classroom: Classroom):
        partners.group_number = classroom.group_number
        for volunteer in partners.volunteers:
            self.unassigned_volunteers.remove(volunteer)
            classroom.assign_volunteer(volunteer)

    def sort_by_availability(self):
        """
        sorts volunteer and partner lists from the least to the greatest classrooms_possible
        """
        for partners in self.partner_groups:
            for classroom in self.classroom_list:
                if can_make_class(partners.free_time, classroom):
                    partners.classrooms_possible += 1

        # for unassigned volunteers, count classrooms they can make, total is Volunteer attribute classrooms_possible
        for person in self.unassigned_volunteers:
            for classroom in self.classroom_list:
                if can_make_class(person.free_time, classroom):
                    person.classrooms_possible += 1

        self.unassigned_volunteers.sort(key=lambda volunteer: volunteer.classrooms_possible)
        self.partner_groups.sort(key=lambda group: group.classrooms_possible)

    def sort_classrooms_by_num_of_volunteers(self):
        self.classroom_list.sort(key=lambda classroom: classroom.num_of_volunteers, reverse=True)

    def assign_team_leaders(self):
        """Assigns team leaders to classroom groups that don't have them. Prioritizes assigning team leaders to
        partially-filled classroom groups over empty classroom groups.

        :return:
        """
        self.sort_classrooms_by_num_of_volunteers()
        for volunteer in self.unassigned_volunteers:
            if volunteer.leader_app:
                class_idx = 0
                while volunteer.group_number == -1 and class_idx < len(self.classroom_list):
                    curr_class = self.classroom_list[class_idx]
                    if can_make_class(volunteer.free_time,
                                      curr_class) and self.max_team_size - curr_class.num_of_volunteers and not curr_class.team_leader:
                        curr_class.assign_volunteer(volunteer)
                        self.unassigned_volunteers.remove(volunteer)
                    else:
                        class_idx += 1
