from applicants.classroom import Classroom
from applicants.teacher import Teacher
from abstract_data_uploader import AbstractDataUploader

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

