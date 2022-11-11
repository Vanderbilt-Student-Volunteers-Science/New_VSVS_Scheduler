import csv
from datetime import datetime, timedelta
from src.partners import Partners
from src.applicant import Volunteer, Classroom


class Scheduler:

    def __init__(self, volunteer_file: str, partner_file: str, classroom_file: str, max_team_size: int = 4,
                 min_team_size: int = 3, travel_time: int = 30):
        """

        :param max_team_size:maximum number of volunteers to allow in a classroom group
        :param min_team_size:minimum acceptable number of volunteers in a classroom group that can visit a classroom
        :param travel_time:minutes to travel one-way to any school
        """
        self.volunteer_list = []
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
        self.assign_team_leaders()
        self.assign_volunteers()
        self.assign_second_time()

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

    def assign_volunteers(self):
        """Assigns all unassigned volunteers to classroom groups. Prioritizes assigning each volunteer to a partially-filled
          classroom group over an empty classroom group.

          :param sorted_others: a list of unassigned volunteers sorted from the fewest to the greatest number of classrooms
          they can make
          :return:
          """
        for volunteer in self.volunteer_list:
            self.sort_classrooms_by_num_of_volunteers()
            classroom_idx = 0
            while volunteer.group_number == -1 and classroom_idx < len(self.classroom_list):
                classroom = self.classroom_list[classroom_idx]
                if classroom.can_make_class(volunteer) and classroom.num_of_volunteers < self.max_team_size:
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
                print(f"WARNING:{partners.volunteers} partner group could not be assigned together because of "
                      "scheduling conflicts.")
        self.sort_by_availability()

    def sort_by_availability(self):
        """
        sorts volunteer and partner lists from the least to the greatest classrooms_possible
        """
        for partners in self.partner_groups:
            for classroom in self.classroom_list:
                if classroom.can_make_class(partners.free_time):
                    partners.classrooms_possible += 1

        # for unassigned volunteers, count classrooms they can make, total is Volunteer attribute classrooms_possible
        for person in self.volunteer_list:
            for classroom in self.classroom_list:
                if classroom.can_make_class(person.free_time):
                    person.classrooms_possible += 1

        self.volunteer_list.sort(key=lambda volunteer: volunteer.classrooms_possible)
        self.partner_groups.sort(key=lambda group: group.classrooms_possible)

    def sort_classrooms_by_num_of_volunteers(self):
        self.classroom_list.sort(key=lambda classroom: classroom.num_of_volunteers, reverse=True)

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
