import src.globalAttributes
import src.classroom
import src.convertSchedule


class Volunteer:
    def __init__(self, first, last, phone, email, year_in_school, major, robotics_interest, special_needs_interest, applied_t_leader, car_passengers, imported_schedule):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.year_in_school = year_in_school
        self.major = major
        self.robotics_interest = robotics_interest
        self.special_needs_interest = special_needs_interest
        self.applied_t_leader = applied_t_leader # if they applied to be a team leader
        if car_passengers == '':
            self.car_passengers = 0
        elif car_passengers == '4+':
            self.car_passengers = 4
        else:
            self.car_passengers = int(car_passengers)
        self.driver = (self.car_passengers >= src.globalAttributes.MAX_TEAM_SIZE)  # can drive if needed
        self.schedule_array = src.convertSchedule.convert_to_schedule_array(imported_schedule)  # array of 1's and 0's
        self.schedule = src.convertSchedule.convert_schedule_array(self.schedule_array)  # array of minutes of consecutive free time after each time
        self.group_number = -1
        self.partners = 0  # Number of other partners (NOT including this Volunteer) Volunteer applied with, set in add_partners method. This is only set for the Volunteer that signed the partners up
        self.partner_indexes = []  # index of each partner in volunteer_list
        self.partner_schedule = 0  # Partner object. This is only set for the Volunteer that signed the partners up.
        self.assigned_driver = 0
        self.assigned_t_leader = 0  # assigned to be a team leader
        self.classrooms_possible = 0 # number of classrooms Volunteer can make based off of their schedule

    def add_partners(self, partner1_email, partner2_email, partner3_email):
        partner1_email = partner1_email.lower()
        partner2_email = partner2_email.lower()
        partner3_email = partner3_email.lower()

        for volunteer_index in range(len(src.globalAttributes.volunteer_list)):
            volunteer = src.globalAttributes.volunteer_list[volunteer_index]
            if volunteer.email == partner1_email or volunteer.email == partner2_email or volunteer.email == partner3_email:
                self.partner_indexes.append(volunteer_index)

        self.partners = len(self.partner_indexes)

        self.partner_schedule = src.convertSchedule.create_partner_schedule(self.schedule_array, self.partners, self.partner_indexes)

    def increment_classrooms_possible(self):
        self.classrooms_possible += 1

    def set_group_number(self, group_number):
        self.group_number = group_number

    def assign_driver(self):
        self.assigned_driver = 1

    def assign_t_leader(self):
        self.assigned_t_leader = 1
