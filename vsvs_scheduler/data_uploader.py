import csv, os, logging
from teacher import Teacher
from classroom import Classroom
from volunteer import Volunteer
from schedule import Schedule
from partners import Partners
from globals import CLASSROOM_RAW_DATA_FILE, TEACHER_COLUMNS, VOLUNTEER_COLUMNS, VOLUNTEER_RAW_DATA_FILE, PARTNER_RAW_DATA_FILE, PARTNER_COLUMNS


class DataUploader():
    """
    The DataUploader class is responsible for importing and processing data from CSV files.
    It creates instances of Teacher, Classroom, Volunteer, and Partners based on the data.
    """

    def __init__(self):
        """
        Initializes the DataUploader with empty lists for classrooms, partners, volunteers, and partners_not_found.
        """
        logging.info('Initializing DataUploader...')
        
        self.classrooms = []
        self.partners = []
        self.volunteers = []
        self.partners_not_found = []



    def import_data(self):
        """
        Imports data from CSV files. The files are defined in the globals.py file.
        Raises FileNotFoundError if a file does not exist.
        Raises ValueError if an invalid file name is encountered.
        """
        logging.info('Importing data from CSV files...')
        logging.debug(f'Current directory {os.path.abspath(os.getcwd())}')
        logging.debug(f'Files to import: {CLASSROOM_RAW_DATA_FILE}, {VOLUNTEER_RAW_DATA_FILE}, {PARTNER_RAW_DATA_FILE}')

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

        logging.info('Data imported successfully.')
        logging.debug(f'Total classrooms: {len(self.classrooms)}, Total volunteers: {len(self.volunteers)}, Total partners: {len(self.partners)}')
    
    
    def process_classroom_data(self, row: dict):
        """
        Processes a row of classroom data from the CSV file.
        Creates a Teacher and Classroom instance for each class a teacher has.
        Adds the Classroom instance to the classrooms list.
        """
        logging.debug(f'{row[TEACHER_COLUMNS.NAME.value]} -- no. classes: {row[TEACHER_COLUMNS.NUM_CLASSES.value]}')

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
        """
        Processes a row of volunteer data from the CSV file.
        Creates a Volunteer instance and adds it to the volunteers list.
        """
        logging.debug(f'{row[VOLUNTEER_COLUMNS.FIRST_NAME.value]} {row[VOLUNTEER_COLUMNS.LAST_NAME.value]}')


        volunteer = Volunteer(
            first        = row[VOLUNTEER_COLUMNS.FIRST_NAME.value].strip().lower().capitalize(),
            last         = row[VOLUNTEER_COLUMNS.LAST_NAME.value].strip().lower().capitalize(),
            phone        = row[VOLUNTEER_COLUMNS.PHONE.value],
            email        = row[VOLUNTEER_COLUMNS.EMAIL.value].strip(),
            leader_app   = (lambda x: True if x == 'Yes' else False)(row[VOLUNTEER_COLUMNS.LEADER.value]),
            schedule     = Schedule(list(row.values())[15:55]),
            board_member = (lambda current_board_member: True if current_board_member == 'Yes' else False)(row[VOLUNTEER_COLUMNS.BOARD.value])
        )

        logging.debug(f'{volunteer.availability}')

        self.volunteers.append(volunteer)
    
    def process_partner_data(self, row: dict):
        """
        Processes a row of partner data from the CSV file.
        Creates a Partners instance if there is more than one partner in a group.
        Adds the Partners instance to the partners list.
        If the number of partners in the group is less than the number specified in the CSV file,
        adds the partner emails to the partners_not_found list.
        """

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








