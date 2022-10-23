class Volunteer:
    """ This class stores volunteer information"""

    def __init__(self, name: str, phone: str, email: str, team_leader_app: bool, index: int, free_time: dict):
        """

        :param name:
        :param phone:
        :param email:
        :param team_leader_app: Did they apply to be a team leader? Yes=true, No=false
        :param index: volunteer index in the volunteer_list
        :param imported_schedule:A list with an element for each 15-min block. The elements in the list are each a
                                  string of letters. The letters in the string indicate the days of the week during
                                  which the volunteer is not available for that time block.
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.leader_app = team_leader_app
        self.index = index
        self.free_time = free_time

        # Defaults
        self.group_number = -1  # group number of -1 means not assigned to a group
        self.robotics = False
        self.special_needs = False
        self.classrooms_possible = 0  # Number of classrooms the volunteer can make according to their schedule
        self.leader = False  # Was the volunteer assigned to be their group's team leader?

        # TODO Convert directly from input schedule to free_time_array in one method. Don't need convert_to_schedule_array.

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is the minutes of consecutive free time the volunteer has starting at that time
        # self.free_time_array = src.convertSchedule.convert_to_free_time_array(self.schedule_array)

        # Was the volunteer assigned to be their group's team leader?
        self.assigned_t_leader = False

        # Number of classrooms the volunteer can make according to their schedule.
        # Set after partners and drivers are assigned.

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
    def set_group_number(self, group_number):
        self.group_number = group_number

    # Designate the volunteer as the team leader for their group
    def assign_t_leader(self):
        self.assigned_t_leader = True

    def __str__(self):
        return self.name


