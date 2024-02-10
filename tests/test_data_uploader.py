import pytest
from src.data_uploader import DataUploader
from src.globals import TEACHER_COLUMNS, VOLUNTEER_COLUMNS

@pytest.fixture
def data_uploader():
    return DataUploader()


def test_process_volunteer_data(data_uploader, volunteerA_data):
    data_uploader.process_volunteer_data(volunteerA_data)

    assert len(data_uploader.volunteers) == 1

    assert data_uploader.volunteers[0].first == volunteerA_data[VOLUNTEER_COLUMNS.FIRST_NAME.value]
    assert data_uploader.volunteers[0].last == volunteerA_data[VOLUNTEER_COLUMNS.LAST_NAME.value]
    assert data_uploader.volunteers[0].email == volunteerA_data[VOLUNTEER_COLUMNS.EMAIL.value]
    assert data_uploader.volunteers[0].phone == volunteerA_data[VOLUNTEER_COLUMNS.PHONE.value]
    assert data_uploader.volunteers[0].board == False

        

def test_process_classroom_data(data_uploader, classroom_data): 
    data_uploader.process_classroom_data(classroom_data)
    assert len(data_uploader.classrooms) == 2
    assert len(data_uploader.classrooms[0].teacher.classrooms) == 2

    assert data_uploader.classrooms[0].teacher.name == classroom_data[TEACHER_COLUMNS.NAME.value]
    assert data_uploader.classrooms[0].teacher.email == classroom_data[TEACHER_COLUMNS.EMAIL.value]
    assert data_uploader.classrooms[0].teacher.phone == classroom_data[TEACHER_COLUMNS.PHONE.value]
    assert data_uploader.classrooms[0].teacher.school == classroom_data[TEACHER_COLUMNS.SCHOOL.value]

    assert len(data_uploader.classrooms[0].teacher.classrooms) == int(classroom_data[TEACHER_COLUMNS.NUM_CLASSES.value])
    assert data_uploader.classrooms[0].start_time.strftime('%I:%M:%S %p') == '0' + classroom_data['Start Time (Class 1 of 2)']
    assert data_uploader.classrooms[0].end_time.strftime('%I:%M:%S %p') == classroom_data['End Time (Class 1 of 2)']
   
    assert data_uploader.classrooms[1].start_time.strftime('%I:%M:%S %p') == classroom_data['Start Time (Class 2 of 2)']
    assert data_uploader.classrooms[1].end_time.strftime('%I:%M:%S %p') == classroom_data['End Time (Class 2 of 2)']



def test_process_partner_data(data_uploader, partner_data, volunteerA_data, volunteerB_data):
    data_uploader.process_volunteer_data(volunteerA_data)
    data_uploader.process_volunteer_data(volunteerB_data)
    data_uploader.process_partner_data(partner_data)

    assert len(data_uploader.partners) == 1
    assert len(data_uploader.partners[0].members) == 2
    assert data_uploader.partners[0].members[0].email == 'jane.smith@example.com'
    assert data_uploader.partners[0].members[1].email == 'john.doe@example.com'


