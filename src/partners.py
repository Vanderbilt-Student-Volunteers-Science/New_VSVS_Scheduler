import src.convertSchedule


class Partners: # object used as a variable for people that filled out the partner application for them and their partners
    def __init__(self, partner1, partner2, partner3, partner_schedule):

        self.partners = 1
        self.partner1 = partner1

        if partner2.isnumeric(): # not "NULL"
            self.partner2 = partner2
            self.partners = 2
        else:
            self.partner2 = 0

        if partner3.isnumeric():
            self.partner3 = partner3
            self.partners = 3
        else:
            self.partner3 = 0

        self.partner_schedule = src.convertSchedule.convert_schedule_array(partner_schedule)
