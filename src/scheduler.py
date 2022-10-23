import csv
from datetime import datetime, timedelta

from src.classroom import Classroom
from src.partners import Partners
from src.volunteer import Volunteer


def can_make_class(schedule: dict, classroom: Classroom):
    day = classroom.weekday
    time = classroom.start_time.strftime('%H:%M')
    if schedule[day][time]:
        return schedule[day][time] >= classroom.duration
    else:
        return False


class Scheduler:
    volunteer_list = []
    classroom_list = []
    partner_groups = []

    def __init__(self, max_team_size: int = 4, min_team_size: int = 3, travel_time: int = 15):
        """

        :param max_team_size:maximum number of volunteers to allow in a classroom group
        :param min_team_size:minimum acceptable number of volunteers in a classroom group that can visit a classroom
        :param travel_time:minutes to travel one-way to any school
        """

        self.max_team_size = max_team_size
        self.min_team_size = min_team_size
        self.travel_time = travel_time
        self.first_time = "07:15"
        self.last_time = "15:30"

    def import_volunteers(self, file_name: str):
        """reads csv with volunteer information and creates a Volunteer object from each row

        :param file_name: filepath to the csv with volunteer info
        :return:
        """
        with open(file_name) as individuals_csv:  # opens file as individuals_csv
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
                    free_time=self.schedule_to_free_time(schedule)
                )
                self.volunteer_list.append(volunteer)

        print('There are {} volunteers.'.format(len(self.volunteer_list)))

    def import_classrooms(self, filename: str):
        """

        :param filename:
        :return:
        """
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
                                          teacher=teacher_name,
                                          phone=teacher_phone,
                                          school=school,
                                          email=email,
                                          start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                                          end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                                          )
                    self.classroom_list.append(classroom)
            print('There are {} classrooms.'.format(len(self.classroom_list)))

    def import_partners(self, file_name: str):
        """

        :param file_name:
        :return:
        """
        with open(file_name) as partners_csv:  # opens partners.csv as partners_csv
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

    def convert_imported_list_to_schedule(self, raw_schedule: list):
        """Converts the schedule imported from individuals.csv into a schedule_dictionary.

        :param raw_schedule: each element represents a 15-min block & the letters are the weekdays the volunteer is busy
        :return: dictionary with a list of times that volunteer is busy for each weekday
        """
        # list of times for each of day of the week that volunteer is unavailable
        weekly_schedule = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}
        start_time = datetime.strptime(self.first_time, "%H:%M")
        end_time = datetime.strptime(self.last_time, "%H:%M")

        current_time = start_time
        idx = 0
        while current_time < end_time:
            if 'M' in raw_schedule[idx]:
                weekly_schedule['Monday'].append(current_time)
            if 'T' in raw_schedule[idx]:
                weekly_schedule['Tuesday'].append(current_time)
            if 'W' in raw_schedule[idx]:
                weekly_schedule['Wednesday'].append(current_time)
            if 'R' in raw_schedule[idx]:
                weekly_schedule['Thursday'].append(current_time)
            current_time = current_time + timedelta(minutes=15)
            idx += 1
        return weekly_schedule

    def schedule_to_free_time(self, schedule: list):
        """

        :param schedule:
        :return:
        """
        unavailability_schedule = self.convert_imported_list_to_schedule(schedule)
        start_time = datetime.strptime(self.first_time, "%H:%M")
        end_time = datetime.strptime(self.last_time, "%H:%M")

        # each day of the week has a dictionary with a key corresponding to the time of day and a value corresponding
        # the minutes of consecutive free time the volunteer has starting at that time
        weekly_free_time = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}}

        for day in unavailability_schedule:  # for each weekday
            current_time = start_time
            day_free_time = weekly_free_time[day]  # dictionary that will keep track of free time for that weekday
            if unavailability_schedule[day]:  # checks that the unavailability schedule for the day exists/ is nonempty
                idx = 0
                next_unavailable_time = unavailability_schedule[day][idx]
            else:
                next_unavailable_time = end_time  # if no unavailability schedule for day, person is available all day
            while current_time < end_time:
                while next_unavailable_time >= current_time:
                    time_available = int((next_unavailable_time - current_time).total_seconds() / 60)  # time in minutes
                    if time_available > 0:
                        # adds free time left from current time into current weekday dictionary in weekly_free_time
                        day_free_time[current_time.strftime('%H:%M')] = time_available
                    current_time += timedelta(minutes=15)  # increases current time by 15 minutes
                if next_unavailable_time == end_time:
                    pass  # no need to check next unavailable time in unavailability_schedule
                elif idx == len(unavailability_schedule[day]) - 1 and unavailability_schedule[day][idx] != end_time:
                    next_unavailable_time = end_time  # if no more unavailability, next unavailable time is end of day
                else:
                    idx += 1
                    next_unavailable_time = unavailability_schedule[day][idx]  # check next unavailable time

        return weekly_free_time

    def assign_partners(self):
        for partners in self.partner_groups:
            class_idx = 0
            while partners.group_number == -1 and class_idx < len(self.classroom_list):
                curr_class = self.classroom_list[class_idx]
                if can_make_class(partners.free_time, curr_class) & (self.max_team_size - curr_class.num_of_volunteers):
                    curr_class.assign_partners(partners)
                else:
                    class_idx += 1
            if partners.group_number == -1:
                print("WARNING: " + partners.volunteers + "partner group could not be assigned together because of "
                                                          "scheduling conflicts.")

    def classrooms_possible_for_volunteer(self, volunteer: Volunteer):
        for volunteer in self.volunteer_list:
            for classroom in self.classroom_list:
                if can_make_class(volunteer.free_time, classroom):
                    volunteer.classrooms_possible += 1

    def classrooms_possible_for_partners(self, partners: Partners):
        for partners in self.partner_groups:
            for classroom in self.classroom_list:
                if can_make_class(partners.free_time, classroom):
                    partners.classrooms_possible += 1

    def sort_by_availability(self):
        """
        sorts volunteer and partner lists from the least to the greatest classrooms_possible
        """
        self.volunteer_list.sort(key=lambda volunteer: volunteer.classrooms_possible)
        self.partner_groups.sort(key=lambda group: group.classrooms_possible)
