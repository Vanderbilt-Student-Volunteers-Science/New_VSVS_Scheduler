import pytest
from vsvs_scheduler.globals import TEACHER_COLUMNS, VOLUNTEER_COLUMNS, PARTNER_COLUMNS

@pytest.fixture
def classroom_data():
    return {
        TEACHER_COLUMNS.EMAIL.value       : 'john.doe@example.com',
        TEACHER_COLUMNS.NAME.value        : 'John Doe',
        TEACHER_COLUMNS.PHONE.value       : '1234567890',
        TEACHER_COLUMNS.SCHOOL.value      : 'ABC School',
        TEACHER_COLUMNS.NUM_CLASSES.value : '2',
        'Days (Class 1 of 2) [1st Preference]': 'Monday',
        'Days (Class 1 of 2) [2nd Preference]': 'Wednesday',
        'Days (Class 1 of 2) [3rd Preference]': 'Thursday',
        'Days (Class 1 of 2) [4th Preference]': 'Tuesday',
        'Start Time (Class 1 of 2)': '9:00:00 AM',
        'End Time (Class 1 of 2)': '10:00:00 AM',
        'Days (Class 2 of 2) [1st Preference]': 'Tuesday',
        'Days (Class 2 of 2) [2nd Preference]': 'Thursday',
        'Days (Class 2 of 2) [3rd Preference]': 'Friday',
        'Days (Class 2 of 2) [4th Preference]': 'Monday',
        'Start Time (Class 2 of 2)': '10:00:00 AM',
        'End Time (Class 2 of 2)': '11:00:00 AM'
    }

@pytest.fixture
def volunteerA_data():
    return {
        'Timestamp'                   : '1/8/2024 12:00:00',
        VOLUNTEER_COLUMNS.EMAIL.value : 'jane.smith@example.com',
        'FAQ Acknowledgement'         : 'Yes',
        'Dress Code Acknowledgement'  : 'Yes',
        VOLUNTEER_COLUMNS.FIRST_NAME.value : 'Jane',
        VOLUNTEER_COLUMNS.LAST_NAME.value: 'Smith',
        VOLUNTEER_COLUMNS.PHONE.value: '9876543210',
        'School': 'School of Engineering',
        'Year': 'Senior',
        'Major': 'Computer Science',
        'Special Needs' : 'No',
        'T-Shirt Size': 'M',
        VOLUNTEER_COLUMNS.BOARD.value: 'No',
        VOLUNTEER_COLUMNS.LEADER.value: 'Yes',
        'Previous Experience (Leader)': 'Yes',
        'Commitments [7:15-7:30 am]' : "Monday, Wednesday",
        'Commitments [7:30-7:45 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [7:45-8:00 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:00-8:15 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:15-8:30 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:30-8:45 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:45-9:00 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:00-9:15 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:15-9:30 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:30-9:45 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:45-10:00 am]' : "Monday, Wednesday, Thursday",
        'Commitments [10:00-10:15 am]': "Monday, Wednesday, Thursday",
        'Commitments [10:15-10:30 am]': "Monday, Wednesday, Thursday",
        'Commitments [10:30-10:45 am]': "Monday, Wednesday, Thursday",
        'Commitments [10:45-11:00 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:00-11:15 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:15-11:30 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:30-11:45 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:45-12:00 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:00-12:15 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:15-12:30 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:30-12:45 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:45-1:00 pm]' : "Monday, Wednesday, Thursday",
        'Commitments [1:00-1:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [1:15-1:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [1:30-1:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [1:45-2:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:00-2:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:15-2:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:30-2:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:45-3:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:00-3:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:15-3:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:30-3:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:45-4:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:00-4:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:15-4:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:30-4:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:45-5:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [5:00-5:15 pm]'  : "Monday, Wednesday, Thursday" 
    }

@pytest.fixture
def volunteerB_data():
    return {
        'Timestamp'                   : '1/8/2024 12:00:00',
        VOLUNTEER_COLUMNS.EMAIL.value : 'john.doe@example.com',
        'FAQ Acknowledgement'         : 'Yes',
        'Dress Code Acknowledgement'  : 'Yes',
        VOLUNTEER_COLUMNS.FIRST_NAME.value : 'John',
        VOLUNTEER_COLUMNS.LAST_NAME.value: 'Doe',
        VOLUNTEER_COLUMNS.PHONE.value: '9876543210',
        'School': 'School of Engineering',
        'Year': 'Senior',
        'Major': 'Computer Science',
        'Special Needs' : 'No',
        'T-Shirt Size': 'M',
        VOLUNTEER_COLUMNS.BOARD.value: 'No',
        VOLUNTEER_COLUMNS.LEADER.value: 'Yes',
        'Previous Experience (Leader)': 'Yes',
        'Commitments [7:15-7:30 am]' : "Monday, Wednesday",
        'Commitments [7:30-7:45 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [7:45-8:00 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:00-8:15 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:15-8:30 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:30-8:45 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [8:45-9:00 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:00-9:15 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:15-9:30 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:30-9:45 am]'  : "Monday, Wednesday, Thursday",
        'Commitments [9:45-10:00 am]' : "Monday, Wednesday, Thursday",
        'Commitments [10:00-10:15 am]': "Monday, Wednesday, Thursday",
        'Commitments [10:15-10:30 am]': "Monday, Wednesday, Thursday",
        'Commitments [10:30-10:45 am]': "Monday, Wednesday, Thursday",
        'Commitments [10:45-11:00 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:00-11:15 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:15-11:30 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:30-11:45 am]': "Monday, Wednesday, Thursday",
        'Commitments [11:45-12:00 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:00-12:15 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:15-12:30 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:30-12:45 pm]': "Monday, Wednesday, Thursday",
        'Commitments [12:45-1:00 pm]' : "Monday, Wednesday, Thursday",
        'Commitments [1:00-1:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [1:15-1:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [1:30-1:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [1:45-2:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:00-2:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:15-2:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:30-2:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [2:45-3:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:00-3:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:15-3:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:30-3:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [3:45-4:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:00-4:15 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:15-4:30 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:30-4:45 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [4:45-5:00 pm]'  : "Monday, Wednesday, Thursday",
        'Commitments [5:00-5:15 pm]'  : "Monday, Wednesday, Thursday"
    }

@pytest.fixture
def partner_data():
    return {
        PARTNER_COLUMNS.NUM_PARTNERS.value : '2',
        PARTNER_COLUMNS.EMAIL.value        : 'john.doe@example.com',
        'Group Member #2': 'jane.smith@example.com'
    }
