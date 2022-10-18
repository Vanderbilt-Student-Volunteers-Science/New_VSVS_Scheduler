import csv

import src.classroom
import src.convertSchedule
from src import volunteer_list


def import_partners(file_name: str):
    """

    :param file_name:
    :return:
    """
    with open(file_name) as partners_csv:  # opens partners.csv as partners_csv
        # returns each row in the csv as a dictionary. The first row in the csv is used for the keys of the dictionary
        csv_reader = csv.DictReader(partners_csv)
        for row in csv_reader:  # for each group of partners
            number_of_partners = int(row['Number of Partners'])  # number of partners in the group
            group = []  # list of the partner volunteer objects
            for i in range(number_of_partners):  # for each partner in the group
                volunteer_found = False
                volunteer_index = 0
                while volunteer_index < len(volunteer_list) and not volunteer_found:
                    volunteer = volunteer_list[volunteer_index]
                    volunteer_index += 1
                    if row[f'Group Member #{i + 1}'].lower() == volunteer.email:
                        volunteer_found = True
                        group.append(volunteer)  # add the volunteer object for the partner to the group list
                    # if we've iterated through the entire list, and we can't find the partner
                    elif volunteer == volunteer_list[-1]:
                        print(f'WARNING: Group Member #{i + 1} ' + row[f'Group Member #{i + 1}'] + 'in group was not '
                                                                                                   'found in '
                                                                                                   'individual '
                                                                                                   'application data.')
            if len(group) > 1:
                group[0].add_partners(group)


class Volunteer:
    """ This class is derived from the Applicant class and stores volunteer information"""

    def __init__(self, name: str, phone: str, email: str, team_leader_app: bool, index: int, free_time: dict):
        """

        :param name:
        :param phone:
        :param email:
        :param team_leader_app: Did they apply to be a team leader? Yes=true, No=false
        :param index:
        :param imported_schedule:A list with an element for each 15-min block. The elements in the list are each a
                                  string of letters. The letters in the string indicate the days of the week during
                                  which the volunteer is not available for that time block.
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.group_number = -1  # group number of -1 means not assigned to a group
        self.robotics = False
        self.special_needs = False
        self.classrooms_possible = 0  # Number of classrooms the volunteer can make according to their schedule
        self.index = index

        # dictionary with a list of 15 minute time blocks that volunteer is busy
        self.free_time = free_time
        self.leader_app = team_leader_app
        self.leader = False  # Was the volunteer assigned to be their group's team leader?

        # TODO Convert directly from input schedule to free_time_array in one method. Don't need convert_to_schedule_array.

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is the minutes of consecutive free time the volunteer has starting at that time
        # self.free_time_array = src.convertSchedule.convert_to_free_time_array(self.schedule_array)

        # The number of other partners (NOT including this Volunteer) Volunteer applied with, set in add_partners
        # method. This is only set in the Volunteer object of the first partner in the group.
        self.partners = 0

        # Index of each of this volunteer's partners in volunteer_list.
        # Set in add_partners method. This is only set in the Volunteer object of the first partner in the group.
        self.partner_indexes = []

        # free_time_array for a partner group.
        # This is only set in the Volunteer object of the first partner in the group.
        self.partner_free_time_array = 0

        # Was the volunteer assigned to be their group's team leader?
        self.assigned_t_leader = False

        # Number of classrooms the volunteer can make according to their schedule.
        # Set after partners and drivers are assigned.
        self.classrooms_possible = 0

    # def add_partners(self, group: list):
    #     """
    #     Sets the partners, partner_indexes, and partner_free_time_array attributes for the Volunteer object of the first
    #     partner in the group (the self object)
    #
    #     :param group:
    #     :return:
    #     """
    #     self.partners = len(group)
    #     for partner in group:
    #         self.partner_indexes.append(partner.index)
    #     if self.partners != 0:
    #         self.partner_free_time_array = src.convertSchedule.create_partner_schedule(self.schedule_array,
    #                                                                                    self.partners,
    #                                                                                    self.partner_indexes)

    def increment_classrooms_possible(self):
        self.classrooms_possible += 1

    def set_group_number(self, group_number):
        self.group_number = group_number

    # Designate the volunteer as the team leader for their group
    def assign_t_leader(self):
        self.assigned_t_leader = True

    def __str__(self):
        return self.name


class Partners:
    def __init__(self, volunteer_list: list):
        self.volunteers = volunteer_list
        self.group_size = len(volunteer_list)
        self.free_time = self.create_partner_schedule(volunteer_list)

    def create_partner_schedule(self, volunteers: list):
        free_time = volunteers[0].freetime
        idx = 1
        while idx < self.group_size:
            for day in free_time:
                for time in day:
                    if time not in volunteers[idx].free_time:
                        del free_time[time]
            idx += 1
        return free_time
