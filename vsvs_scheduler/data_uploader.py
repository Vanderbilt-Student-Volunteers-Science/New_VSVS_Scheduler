import csv
import os
from applicants.teacher import Teacher
from applicants.classroom import Classroom
from applicants.volunteer import Volunteer
from applicants.schedule import Schedule
from applicants.partners import Partners
from __init__ import CLASSROOM_RAW_DATA_FILE, TEACHER_COLUMNS, VOLUNTEER_COLUMNS, VOLUNTEER_RAW_DATA_FILE, PARTNER_RAW_DATA_FILE, PARTNER_COLUMNS


class DataUploader():
    def __init__(self):

        self.classrooms = []
        self.partners = []
        self.volunteers = []
        self.partners_not_found = []
        self.import_data()



    def import_data(self) -> str:
        """ Prompt user for file path to csv/excel file."""

        files = [CLASSROOM_RAW_DATA_FILE, VOLUNTEER_RAW_DATA_FILE, PARTNER_RAW_DATA_FILE]

        for file_name in files:
            if (not os.path.isfile(file_name)):
                raise FileNotFoundError(f"File not found at {file_name}")
            
            print (f"\nImporting {file_name} ...")

            with open(file_name) as current_csv:
                # DictReader creates an ordered dictionary for each row in the csv file
                csv_reader = csv.DictReader(current_csv)

                if file_name is CLASSROOM_RAW_DATA_FILE:
                    for row in csv_reader:
                        self.process_classroom_data(row)
                elif file_name is VOLUNTEER_RAW_DATA_FILE:
                    for row in csv_reader:
                        self.process_volunteer_data(row)
                elif file_name is PARTNER_RAW_DATA_FILE:
                    for row in csv_reader:
                        self.process_partner_data(row)
                else:
                    raise ValueError(f"Invalid file name: {file_name}")
    
    
    def process_classroom_data(self, row: dict):
        """ Process row data from csv/excel file into Classroom objects."""
        group_num = 0

        number_of_classes = int(row[TEACHER_COLUMNS.NUM_CLASSES.value])

        teacher = Teacher (
            name   = row[TEACHER_COLUMNS.NAME.value],
            phone  = row[TEACHER_COLUMNS.PHONE.value],
            school = row[TEACHER_COLUMNS.SCHOOL.value],
            email  = row[TEACHER_COLUMNS.EMAIL.value],
            weekday_preferences=[
                    row[f'Days (Class {number_of_classes} of {number_of_classes}) [1st Preference]'],
                    row[f'Days (Class {number_of_classes} of {number_of_classes}) [2nd Preference]'],
                    row[f'Days (Class {number_of_classes} of {number_of_classes}) [3rd Preference]'],
                    row[f'Days (Class {number_of_classes} of {number_of_classes}) [4th Preference]']
                ]
            )

       # for each class a teacher has, create a classroom object and add it to the list 'applicants'
        for i in range(number_of_classes):
            group_num += 1
            class_num = i + 1  # class_num keeps track of which class out of the total being created
            classroom = Classroom(
                group_number = group_num,
                teacher      = teacher,
                start_time   = row[f'Start Time (Class {class_num} of {number_of_classes})'],
                end_time     = row[f'End Time (Class {class_num} of {number_of_classes})']  
            )
            teacher.add_classrooms(classroom)

            self.classrooms.append(classroom)
    
    def process_volunteer_data(self, row: dict):
        volunteer = Volunteer(
            first        = row[VOLUNTEER_COLUMNS.FIRST_NAME.value].strip().lower().capitalize(),
            last         = row[VOLUNTEER_COLUMNS.LAST_NAME.value].strip().lower().capitalize(),
            phone        = row[VOLUNTEER_COLUMNS.PHONE.value],
            email        = row[VOLUNTEER_COLUMNS.EMAIL.value].strip(),
            leader_app   = (lambda x: True if x == 'Yes' else False)(row[VOLUNTEER_COLUMNS.LEADER.value]),
            schedule     = Schedule(list(row.values())[15:55]),
            board_member = (lambda current_board_member: True if current_board_member == 'Yes' else False)(row[VOLUNTEER_COLUMNS.BOARD.value])
        )

        self.volunteers.append(volunteer)
    
    def process_partner_data(self, row: dict):
        """ Process row data from csv/excel file into Partner objects."""

        number_of_partners = int(row[PARTNER_COLUMNS.NUM_PARTNERS.value])
        partner_emails = [row[PARTNER_COLUMNS.EMAIL.value].lower()]

        # add all the partners' emails to the list 'partner_emails'
        for i in range(1, number_of_partners): 
            partner_email = row[f'Group Member #{i + 1}'].lower()
            partner_emails.append(partner_email)

        # create a list of volunteers that are in the partner group
        group = [volunteer for volunteer in self.volunteers if (volunteer.email in partner_emails)]

        # Remove duplicate volunteers
        for partner in group:
            duplicates = [partner_group for partner_group in self.partners if partner in partner_group.members]
            if len(duplicates) != 0 and len(group) > 1:
                    print(f'{partner.email} was in 2 groups. One deleted.')
                    self.partners.remove(duplicates[0])

        if len(group) > 1:
            self.partners.append(Partners(group))
        
        if len(group) < number_of_partners:
            self.partners_not_found.append(partner_emails)








