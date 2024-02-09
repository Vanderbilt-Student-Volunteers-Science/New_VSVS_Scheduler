from enum import Enum

# Column names in the data in the teacher and volunteer application CSV file
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

# File paths for the raw application data
CLASSROOM_RAW_DATA_FILE = "data/classrooms.csv"
VOLUNTEER_RAW_DATA_FILE = "data/individuals.csv"
PARTNER_RAW_DATA_FILE   = "data/partners.csv"

# Directory where the assignments are stored
ASSIGNMENTS_DIRECTORY = "results"

# Constants for the earliest and latest times for scheduling
EARLIEST_TIME = "7:15"
LATEST_TIME = "15:30"

# Duration of each time block in minutes
TIME_BLOCK_DURATION = 15

# Maximum and minimum team sizes
MAX_TEAM_SIZE = 5
MIN_TEAM_SIZE = 3
