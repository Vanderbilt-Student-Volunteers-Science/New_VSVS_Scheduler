import warnings

import src.classroom
import src.convert_schedule
import src.global_attributes


class Volunteer:
    def __init__(self, first, last, phone, email, year_in_school, major,
                 applied_t_leader, board, schedule):
        """ constructor for volunteer object

        :param first: first name
        :type first: str
        :param last: last name
        :type last: str
        :param phone: phone number
        :type phone: str
        :param email: Vanderbilt email address
        :type email: str
        :param year_in_school: year at Vanderbilt (First-Year, Sophomore, Junior, Senior, Graduate)
        :type year_in_school: str
        :param major: major at Vanderbilt
        :type major: str
        :param applied_t_leader: did this volunteer apply to be a team leader?
        :type applied_t_leader: bool
        :param board: is this volunteer on VSVS Board?
        :type board: bool
        :param schedule: raw schedule data from Google Form
        :type schedule: list[str]
        """
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.year_in_school = year_in_school
        self.major = major
        self.applied_t_leader = applied_t_leader
        self.board = board


        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is the minutes of consecutive free time the volunteer has starting at that time
        self.free_time_array = src.convert_schedule.convert_to_free_time_array(schedule)

        # group number of -1 means not assigned to a group
        self._group_number = -1

        # free_time_array for a partner group.
        # This is only set in the Volunteer object of the first partner in the group.
        self.partner_free_time_array = 0

        # Was the volunteer assigned to be their group's team leader?
        self.assigned_t_leader = False

        # Number of classrooms the volunteer can make according to their schedule.
        # Set after partners and drivers are assigned.
        self.classrooms_possible = 0

    # group number is a property (special type of Python variable) so we can have a custom setter method
    @property
    def group_number(self):
        return self._group_number

    @group_number.setter
    def group_number(self, value):
        """

        :param value: new group number
        :type value: int
        :raises ValueError: if re-assigning an already assigned volunteer
        :return:
        """
        if self._group_number != -1:
            raise ValueError("You are changing the group number of an already assigned volunteer.")
        self._group_number = value

    @group_number.deleter
    def group_number(self):
        del self._group_number


    def __str__(self):
        return self.first + ' ' + self.last

    def __repr__(self):
        return self.first + ' ' + self.last
