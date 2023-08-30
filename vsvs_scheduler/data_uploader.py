
import csv
import os
from abc import ABC, abstractmethod
from classroom import Classroom
from teacher import Teacher
from partners import Partners
from volunteer import Volunteer
from schedule import Schedule


class AbstractDataUploader(ABC):
    """ This abstract class is used as base for all the DataUploader classes"""
    
    def __init__(self, applicant_type: str):
        super().__init__()
        self.filename = self.file_prompt(applicant_type)
        self.applicants = []
        


    def file_prompt(self, applicant_file: str) -> str:
        """ Helper function to verify the file specified by the user can be located.
            
            :param: applicant_type: 'individuals', 'partners', or 'classrooms'
            :return: path to file
        """
        filename = input(f"Enter the file path to the {applicant_file} file:\n")

    
        while (not os.path.isfile(filename)):
            if filename == "" or filename is None:
                filename = f"data/{applicant_file}.csv"
            else:  
                filename = input(f"Enter the file path to the {applicant_file} file:\n")

        print(f"\nImporting {applicant_file} ...")

        return filename
    
    def import_data(self):
        """ Open file and use csv reader to create dictionary of the row. The column
            names are the keys in th dictionary.
        """
        with open(self.filename) as current_csv:
            csv_reader = csv.DictReader(current_csv)
            for row in csv_reader:
                self.process_row_data(row)
        
        print (f"\nImport complete. {len(self.applicants)} records added.\n")

    @abstractmethod
    def process_row_data(self, row: dict):
        """ Method to be defined by children class for how to process each row. """
        pass

class VolunteerDataUploader(AbstractDataUploader):
    """ This uploads volunteer data from csv/excel file into Volunteer objects """
    def __init__(self):
        super().__init__("individuals")
        self.import_data()
        
    
    def process_row_data(self, row: dict):
        """ Create volunteer object and append it to list of applicants """
    
        volunteer = Volunteer(
            first=row['First Name'].strip().lower().capitalize(),
            last=row['Last Name'].strip().lower().capitalize(),
            phone=row['Phone Number'],
            email=row['Email Address'].strip(),
            leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
            schedule=Schedule(list(row.values())[15:56]),
            board_member=(lambda current_board_member: True if current_board_member == 'Yes' else False)(row['Board Member'])
        )

        self.applicants.append(volunteer)

class ClassDataUploader(AbstractDataUploader):
    """ This uploads classroom data from csv/excel file into Classroom objects """

    def __init__(self):
        super().__init__("classrooms")
        self.group_num = 0
        self.import_data()

    def process_row_data(self, row: dict):
        number_of_classes = row['Number of Classes']
        teacher = Teacher (
            name= row['Name'],
            phone= row['Cell Phone Number'],
            school= row['School'],
            email=  row['Email Address']
        )

        # For each class that the teacher has we create a Classroom object
        for i in range(int(number_of_classes)):
            self.group_num += 1
            class_num = i + 1  # class_num keeps track of which class out of the total being created
            classroom = Classroom(
                group_number=self.group_num,
                teacher=teacher,
                start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                weekday=row[f'Days (Class {class_num} of {number_of_classes}) [1st Preference]']
            )

            self.applicants.append(classroom)
  

class PartnerDataUploader(AbstractDataUploader):
    """ This uploads partner data from csv/excel file into Partner objects """

    def __init__(self, individual_volunteers: list):
        super().__init__("Partners")
        self.individuals = individual_volunteers
        self.partners_not_found = []
        self.import_data()

    def process_row_data(self, row: dict):
        number_of_partners = int(row['Number of Partners'])
        partner_emails = [row['Email Address'].lower()]

        # for each person in the partners_csv row, add their email to partner_emails
        for i in range(1, number_of_partners): 
            partner_email = row[f'Group Member #{i + 1}'].lower()
            partner_emails.append(partner_email)

        # list comprehension adds all the partners' volunteer objects to the list 'group'
        group = [volunteer for volunteer in self.individuals if (volunteer.email in partner_emails)]

        # Remove duplicates
        for partner in group:
            for partnered in self.applicants:
                if partner in partnered.members and len(group) > 1:
                    print(f'{partner.email} was in 2 groups. One deleted.')
                    self.applicants.remove(partnered)

        if len(group) > 1:
            self.applicants.append(Partners(group))
        
        if len(group) < number_of_partners:
            self.partners_not_found.append(partner_emails)
