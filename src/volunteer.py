import src.globalAttributes
import src.classroom
import src.convertSchedule


class Volunteer:
    def __init__(self, first, last, phone, email, year_in_school, major, robotics_interest, special_needs_interest, applied_t_leader, car_passengers, imported_schedule, is_in_person):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.year_in_school = year_in_school
        self.major = major
        self.robotics_interest = robotics_interest
        self.special_needs_interest = special_needs_interest

        # if volunteer applied to be a team leader
        self.applied_t_leader = applied_t_leader

        # people a driver can drive (not including driver)
        if car_passengers == '':
            self.car_passengers = 0
        elif car_passengers == '4+':
            self.car_passengers = 4
        else:
            self.car_passengers = int(car_passengers)

        # if they have a car that can carry the MAX_TEAM_SIZE
        self.driver = (self.car_passengers + 1 >= src.globalAttributes.MAX_TEAM_SIZE)

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.); value at
        # an index is 1 if volunteer is available at that time and 0 if they are busy
        self.schedule_array = src.convertSchedule.convert_to_schedule_array(imported_schedule)

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.); value at
        # an index is the minutes of consecutive free time the volunteer has starting at that time
        self.free_time_array = src.convertSchedule.convert_to_free_time_array(self.schedule_array)

        # group number of -1 means not assigned to a group
        self.group_number = -1

        # The number of other partners (NOT including this Volunteer) Volunteer applied with, set in add_partners
        # method. This is only set in the Volunteer object of the first partner in the group.
        self.partners = 0

        # Index of each of this volunteer's partners in volunteer_list. Set in add_partners method. This is only set in
        # the Volunteer object of the first partner in the group.
        self.partner_indexes = []

        # free_time_array for a partner group. This is only set in the Volunteer object of the first partner in the
        # group.
        self.partner_free_time_array = 0

        # Was the volunteer assigned to be the driver for their group?
        self.assigned_driver = 0

        # Was the volunteer assigned to be their group's team leader?
        self.assigned_t_leader = 0

        # Number of classrooms the volunteer can make according to their schedule. Set after partners and drivers are
        # assigned.
        self.classrooms_possible = 0

        # True if the volunteer is in person, False if they are remote.
        self.is_in_person = is_in_person

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
        while volunteer_index < len(src.globalAttributes.volunteer_list) and partners_matched == 0:
            volunteer = src.globalAttributes.volunteer_list[volunteer_index]
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
            elif volunteer == src.globalAttributes.volunteer_list[-1]:
                if partner1_matched == 0:
                    print(partner1_email, end = ' ')
                if partner2_matched == 0:
                    print(partner2_email, end = ' ')
                if partner3_matched == 0:
                    print(partner3_email, end = ' ')
                print("from " + self.email + "'s partner group were not found in individual application data.")

        self.partners = len(self.partner_indexes)

        # If all three partners are remote, they cannot be assigned in a group together. At least one volunteer in each group must be in person.
        if self.partners == 2 and not self.is_in_person and not src.globalAttributes.volunteer_list[self.partner_indexes[0]].is_in_person and not src.globalAttributes.volunteer_list[self.partner_indexes[1]].is_in_person:
            print(self.email + "'s partner group cannot be grouped together because they are all remote.")

        elif self.partners != 0:
            self.partner_free_time_array = src.convertSchedule.create_partner_schedule(self.schedule_array, self.partners, self.partner_indexes)

    def increment_classrooms_possible(self):
        self.classrooms_possible += 1

    def set_group_number(self, group_number):
        self.group_number = group_number

    # Designate the volunteer as the team leader for their group
    def assign_t_leader(self):
        self.assigned_t_leader = 1
