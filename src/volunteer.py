import src.partners
import src.convertSchedule


class Volunteer:
    def __init__(self, first, last, phone, email, prev_member, applied_t_leader, prev_t_leader, car_passengers, schedule, robotics, special_needs, preassigned_group=-1):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.prev_member = prev_member
        self.applied_t_leader = applied_t_leader # if they applied to be a team leader
        self.prev_t_leader = prev_t_leader
        self.car_passengers = car_passengers # 0 if no car
        self.schedule = src.convertSchedule.convert_schedule_array(schedule)
        self.robotics = robotics
        self.special_needs = special_needs
        self.group_number = preassigned_group # Do they have a team yet and what is it?
        self.partners = 0  # Number of other partners (NOT including this Volunteer) Volunteer applied with, set in add_partners method. This is only set for the Volunteer that signed the partners up
        self.partner_details = 0  # Partner object. This is only set for the Volunteer that signed the partners up.
        self.t_leader = 0  # assigned to be a team leader
        self.classrooms_possible = 0 # number of classrooms Volunteer can make based off of their schedule

    def add_partners(self, partner1, partner2, partner3, partner_schedule):

        self.partner_details = src.partners.Partners(partner1, partner2, partner3, partner_schedule)

        if self.partner_details.partner[2] == 0:
            self.partners = 1
        elif self.partner_details.partner[3] == 0:
            self.partners = 2
        else:
            self.partners = 3

    def increment_classrooms_possible(self):
        self.classrooms_possible += 1
