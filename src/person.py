import src.partners

class Person:
    def __init__(self, first, last, robotics, next_steps, t_leader, car):
        self.first = first
        self.last = last
        self.robotics = 1 if robotics == "Yes" else 0
        self.next_steps = 1 if next_steps == "Yes" else 0
        self.t_leader = 1 if t_leader == "Yes" else 0
        self.car = 0 if car == "" else (4 if car == "4 or more" else car)  # "" means 0, "4 or more" means 4
        self.onTeam = 0 # Do they have a team yet?
        self.partner_app = 0 # Did they apply with partners? (set in addPartners method) This person is the one that signed the partners up.
        self.partners = 0 # Partner object

    def addPartners(self, partner1, partner2, partner3):
        self.partner_app = 1
        self.partners = src.partners.Partners(partner1, partner2, partner3)
