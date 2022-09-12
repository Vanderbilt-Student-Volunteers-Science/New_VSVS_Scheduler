import src.classroom
import src.convertSchedule
import src.globalAttributes


class Volunteer:
    def __init__(self, first, last, phone, email, robotics_interest, special_needs_interest, leader_app,
                 imported_schedule):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.robotics_interest = robotics_interest
        self.special_needs_interest = special_needs_interest

        # if volunteer applied to be a team leader
        self.leader_app = leader_app

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

        # Was the volunteer assigned to be the driver for their group?
        self.assigned_driver = False

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
        while volunteer_index < len(src.__init__.volunteer_list) and partners_matched == 0:
            volunteer = src.__init__.volunteer_list[volunteer_index]
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
            elif volunteer == src.__init__.volunteer_list[-1]:
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
