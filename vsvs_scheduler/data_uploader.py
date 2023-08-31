
import csv
import os
from abc import ABC, abstractmethod
from classroom import Classroom
from teacher import Teacher
from partners import Partners
from volunteer import Volunteer
from schedule import Schedule


class AbstractDataUploader(ABC):
    def __init__(self, applicant_type: str):
        """ Abstract class for uploading data from csv/excel file into objects."""

        super().__init__()
        self.filename = self.file_prompt(applicant_type)
        self.applicants = []



    def file_prompt(self, applicant_file: str) -> str:
        """ Prompt user for file path to csv/excel file."""

        filename = input(f"Enter the file path to the {applicant_file} file:\n")

        # Keep prompting user until they enter a valid file path
        while (not os.path.isfile(filename)):
            if filename == "" or filename is None:
                filename = f"data/{applicant_file}.csv"
            else:  
                filename = input(f"Enter the file path to the {applicant_file} file:\n")

        print(f"\nImporting {applicant_file} ...")

        return filename
    


    def import_data(self):
        """ Import data from csv/excel file into objects. """

        with open(self.filename) as current_csv:

            # DictReader creates an ordered dictionary for each row in the csv file
            csv_reader = csv.DictReader(current_csv)

            for row in csv_reader:
                self.process_row_data(row)
        
        print (f"\nImport complete. {len(self.applicants)} records added.\n")



    @abstractmethod
    def process_row_data(self, row: dict):
        """ Abstract method for processing row data from csv/excel file into objects. """
        pass






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







class ClassDataUploader(AbstractDataUploader):
    def __init__(self):
        """ This uploads class data from csv/excel file into Classroom objects"""

        super().__init__("classrooms")
        self.group_num = 0
        self.import_data()



    def process_row_data(self, row: dict):
        """ Process row data from csv/excel file into Classroom objects."""

        number_of_classes = row['Number of Classes']
        teacher = Teacher (
            name= row['Name'],
            phone= row['Cell Phone Number'],
            school= row['School'],
            email=  row['Email Address']
        )

       # for each class a teacher has, create a classroom object and add it to the list 'applicants'
        for i in range(int(number_of_classes)):
            self.group_num += 1
            class_num = i + 1  # class_num keeps track of which class out of the total being created
            classroom = Classroom(
                group_number=self.group_num,
                teacher=teacher,
                start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                weekdays=[
                    row[f'Days (Class {class_num} of {number_of_classes}) [1st Preference]'],
                    row[f'Days (Class {class_num} of {number_of_classes}) [2nd Preference]'],
                    row[f'Days (Class {class_num} of {number_of_classes}) [3rd Preference]'],
                    row[f'Days (Class {class_num} of {number_of_classes}) [4th Preference]'],
                ]
                
            )

            self.applicants.append(classroom)





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
