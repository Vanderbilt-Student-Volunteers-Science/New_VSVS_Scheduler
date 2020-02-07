import src.partners


class Person:
    def __init__(self, first, last, phone, email, prev_member, applied_t_leader, prev_t_leader, car_passengers, schedule, robotics, special_needs, preassigned_group=0):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.prev_member = prev_member
        self.applied_t_leader = applied_t_leader # if they applied to be a team leader
        self.prev_t_leader = prev_t_leader
        self.car_passengers = car_passengers # 0 if no car
        self.schedule = schedule
        self.robotics = robotics
        self.special_needs = special_needs
        self.group_number = preassigned_group # Do they have a team yet and what is it?
        self.partner_app = 0 # Did they apply with partners? (set in addPartners method) This person is the one that signed the partners up.
        self.partners = 0 # Partner object
        self.t_leader = 0 # assigned to be a team leader

    def add_partners(self, partner1, partner2, partner3):
        self.partner_app = 1
        self.partners = src.partners.Partners(partner1, partner2, partner3, partner_schedule)
