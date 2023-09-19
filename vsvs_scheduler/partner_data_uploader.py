from abstract_data_uploader import AbstractDataUploader
from applicants.partners import Partners


class PartnerDataUploader(AbstractDataUploader):
    def __init__(self, individual_volunteers: list):
        """ This uploads partner data from csv/excel file into Partner objects"""

        super().__init__("Partners")
        self.individuals = individual_volunteers
        self.partners_not_found = []
        self.import_data()


        
    def process_row_data(self, row: dict):
        """ Process row data from csv/excel file into Partner objects."""

        number_of_partners = int(row['Number of Partners'])
        partner_emails = [row['Email Address'].lower()]

        # add all the partners' emails to the list 'partner_emails'
        for i in range(1, number_of_partners): 
            partner_email = row[f'Group Member #{i + 1}'].lower()
            partner_emails.append(partner_email)

        # create a list of volunteers that are in the partner group
        group = [volunteer for volunteer in self.individuals if (volunteer.email in partner_emails)]

        # Remove duplicate volunteers
        for partner in group:
            for partnered in self.applicants:
                if partner in partnered.members and len(group) > 1:
                    print(f'{partner.email} was in 2 groups. One deleted.')
                    self.applicants.remove(partnered)

        if len(group) > 1:
            self.applicants.append(Partners(group))
        
        if len(group) < number_of_partners:
            self.partners_not_found.append(partner_emails)