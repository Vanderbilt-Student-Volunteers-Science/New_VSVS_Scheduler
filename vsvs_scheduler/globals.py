from enum import Enum

class TEACHER_COLUMNS(Enum):
    NAME        = 'Name'
    PHONE       = 'Cell Phone Number'
    SCHOOL      = 'School'
    EMAIL       = 'Email Address'
    NUM_CLASSES = 'Number of Classes'

class VOLUNTEER_COLUMNS(Enum):
    FIRST_NAME = 'First Name'
    LAST_NAME  = 'Last Name'
    PHONE      = 'Phone'
    EMAIL      = 'Email Address'
    LEADER     = 'Team Leader'
    BOARD      = 'Board Member'

class PARTNER_COLUMNS(Enum):
    NUM_PARTNERS = 'Number of Partners'
    EMAIL        = 'Email Address'


CLASSROOM_RAW_DATA_FILE = "data/classrooms.csv"
VOLUNTEER_RAW_DATA_FILE = "data/individuals.csv"
PARTNER_RAW_DATA_FILE   = "data/partners.csv"

ASSIGNMENTS_DIRECTORY = "results"


EARLIEST_TIME = "7:15"
LATEST_TIME = "15:30"
TIME_BLOCK_DURATION = 15
MAX_TEAM_SIZE = 5
MIN_TEAM_SIZE = 3
