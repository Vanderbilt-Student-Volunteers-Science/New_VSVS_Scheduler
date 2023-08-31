from abstract_data_uploader import AbstractDataUploader
from applicants.schedule import Schedule
from applicants.volunteer import Volunteer


class VolunteerDataUploader(AbstractDataUploader):
    def __init__(self):
        """ This uploads volunteer data from csv/excel file into Volunteer objects """

        super().__init__("individuals")
        self.import_data()



    def process_row_data(self, row: dict):
        """ Process row data from csv/excel file into Volunteer objects."""
    
        volunteer = Volunteer(
            first=row['First Name'].strip().lower().capitalize(),
            last=row['Last Name'].strip().lower().capitalize(),
            phone=row['Phone Number'],
            email=row['Email Address'].strip(),
            leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
            schedule=Schedule(list(row.values())[15:55]),
            board_member=(lambda current_board_member: True if current_board_member == 'Yes' else False)(row['Board Member'])
        )

        self.applicants.append(volunteer)