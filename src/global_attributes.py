# Contains global constants and variables for VSVS Volunteer Sorting Program


# CONSTANTS

# maximum number of volunteers to allow in a classroom group
MAX_TEAM_SIZE = 5

# minimum acceptable number of volunteers in a classroom group that can visit a classroom
MIN_TEAM_SIZE = 3

# minutes to travel one-way to any school
SCHOOL_TRAVEL_TIME = 15

# index for each field in the individuals csv (zero-based)
INDIVIDUAL_INDEX = {
     'FIRST': 4,
     'LAST': 5,
     'PHONE': 6,
     'EMAIL': 7,
     'SCHOOL': 8,
     'YEAR': 9,
     'MAJOR': 10,
     'SPECIAL_NEEDS_INTEREST': 11,
     'APPLIED_T_LEADER': 13,
     'BOARD': 3,
     'IMPORTED_SCHEDULE_START': 16,
     'IMPORTED_SCHEDULE_END': 49,
     'LOCATION': 52
}

CLASSROOM_INDEX = {
     'GROUP_NUMBER': 1,
     'TEACHER_NAME': 3,
     'TEACHER_PHONE': 4,
     'SCHOOL': 6,
     'TEACHER_EMAIL': 9,
     'CLASS_START_TIME': 11,
     'CLASS_END_TIME': 12,
     'DAY_OF_WEEK': 13

}

# Volunteer Schedule Constants
# Each volunteer fills out a Google Form (individuals.csv) where they input their time commitments from
# Monday to Thursday. The schedule starts at 7:15 AM (SCHEDULE_START_TIME) and continues in 15 min blocks
# (SCHEDULE_BLOCK_LENGTH) for 34 (NUMBER_of_PERIODS_PER_DAYS) blocks until 3:45 PM

# duration of each time period in individuals.csv Google Form (minutes)
SCHEDULE_BLOCK_LENGTH = 15

# time that the schedule in the individuals.csv Google Form starts at (in military time)
SCHEDULE_START_TIME = 715

# number of periods of length SCHEDULE_BLOCK_LENGTH for each day that starts at SCHEDULE_START_TIME
BLOCKS_PER_DAY = INDIVIDUAL_INDEX['IMPORTED_SCHEDULE_END'] - INDIVIDUAL_INDEX['IMPORTED_SCHEDULE_START'] + 1

# VARIABLES

# contains all of the Volunteer objects, one for each VSVS volunteer
volunteer_list = []

# contains all of the Classroom objects, one for each VSVS group that needs to be created
classroom_list = []

# contains all Classroom objects that are partially filled; starts being filled after partners and drivers have been
# assigned
partially_filled_classrooms = []

# contains all Classroom objects that are empty; starts being used after partners and drivers have been updated
empty_classrooms = []
