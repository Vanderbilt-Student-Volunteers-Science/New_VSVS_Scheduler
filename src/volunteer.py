import csv

import src.classroom
import src.convertSchedule
from src.__init__ import volunteer_list


def import_volunteer_info(file_name: str):
    """ reads csv with volunteer information and creates a Volunteer object from each row

        :param file_name: filepath to the csv with volunteer info
    """

    with open(file_name, 'r') as individuals_csv:  # opens csv as individuals_csv
        # returns each row in the csv as a dictionary. The first row in the csv is used for the keys of the dictionary
        csv_reader = csv.DictReader(individuals_csv)

        for row in csv_reader:  # for each individual
            # pull data from row in the csv, create a Volunteer object, and add it to global variable volunteer_list
            volunteer = Volunteer(
                first=row['First Name'].strip(),
                last=row['Last Name'].strip(),
                phone=row['Phone Number'],
                email=row['Email'].strip(),
                robotics_interest=False,  # no robotics for Fall 2020
                special_needs_interest=(lambda x: True if x == 'Yes' else False)(row['Special Needs Students']),
                leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
                imported_schedule=list(row.values())[16:50],
            )
            volunteer_list.append(volunteer)

    print('There are {} volunteers.'.format(len(volunteer_list)))


class Volunteer:
    """This class stores volunteer information: first name, last name, phone, email, robotics interest, special needs
    interest, leadership application, schedule """

    def __init__(self, first: str, last: str, phone: str, email: str, robotics_interest: bool,
                 special_needs_interest: bool, leader_app: bool, imported_schedule: list):
        """
        :param first: first name
        :param last: last name
        :param phone: cell phone number
        :param email: vanderbilt email
        :param robotics_interest: Are they interested in robotics? Yes=true, No=false
        :param special_needs_interest: Are they interested in working with special needs students? Yes=true, No=false
        :param leader_app: Did they apply to be a team leader? Yes=true, No=false
        :param imported_schedule: A list with an element for each 15-min block. The elements in the list are each a
                                  string of letters. The letters in the string indicate the days of the week during
                                  which the volunteer is not available for that time block.
        """
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.robotics_interest = robotics_interest
        self.special_needs_interest = special_needs_interest
        self.leader_app = leader_app  # if volunteer applied to be a team leader

        # TODO Convert directly from input schedule to free_time_array in one method. Don't need convert_to_schedule_array.
        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is 1 if volunteer is available at that time and 0 if they are busy
        self.schedule_array = src.convertSchedule.convert_to_schedule_array(imported_schedule)

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is the minutes of consecutive free time the volunteer has starting at that time
        self.free_time_array = src.convertSchedule.convert_to_free_time_array(self.schedule_array)

        # group number of -1 means not assigned to a group
        self.group_number = -1

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

    # Sets the partners, partner_indexes, and partner_free_time_array attributes for the Volunteer object of the first
    # partner in the group (the self object).
    def add_partners(self, partner1_email, partner2_email, partner3_email):
        partner1_email = partner1_email.lower()
        partner2_email = partner2_email.lower()
        partner3_email = partner3_email.lower()

        volunteer_index = 0

        partner1_matched = 0
        partner2_matched = 0
        partner3_matched = 0
        partners_matched = 0
        if partner2_email == '':
            partner2_matched = 1
        if partner3_email == '':
            partner3_matched = 1
        while volunteer_index < len(volunteer_list) and partners_matched == 0:
            volunteer = volunteer_list[volunteer_index]
            if volunteer.email == partner1_email:
                self.partner_indexes.append(volunteer_index)
                partner1_matched = 1
            elif volunteer.email == partner2_email:
                self.partner_indexes.append(volunteer_index)
                partner2_matched = 1
            elif volunteer.email == partner3_email:
                self.partner_indexes.append(volunteer_index)
                partner3_matched = 1

            volunteer_index += 1

            if partner1_matched and partner2_matched and partner3_matched:
                partners_matched = 1
            elif volunteer == volunteer_list[-1]:
                print("WARNING: ", end='')
                if partner1_matched == 0:
                    print(partner1_email, end=' ')
                if partner2_matched == 0:
                    print(partner2_email, end=' ')
                if partner3_matched == 0:
                    print(partner3_email, end=' ')
                print("from " + self.email + "'s partner group were not found in individual application data.")

        self.partners = len(self.partner_indexes)

        if self.partners != 0:
            self.partner_free_time_array = src.convertSchedule.create_partner_schedule(self.schedule_array,
                                                                                       self.partners,
                                                                                       self.partner_indexes)

    def increment_classrooms_possible(self):
        self.classrooms_possible += 1

    def set_group_number(self, group_number):
        self.group_number = group_number

    # Designate the volunteer as the team leader for their group
    def assign_t_leader(self):
        self.assigned_t_leader = True

    def __str__(self):
        return self.first + ' ' + self.last
