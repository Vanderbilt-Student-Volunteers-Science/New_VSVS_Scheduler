# Contains global constants and variables for VSVS Volunteer Sorting Program


# CONSTANTS

# maximum number of volunteers to allow in a classroom group
MAX_TEAM_SIZE = 4

# minimum acceptable number of volunteers in a classroom group that can visit a classroom
MIN_TEAM_SIZE = 3

# minutes to travel one-way to any school
SCHOOL_TRAVEL_TIME = 15

# index for each field in the individuals csv
I = {'FIRST': 3, 'LAST': 4, 'PHONE': 5, 'EMAIL': 6, 'SCHOOL': 7, 'YEAR': 8, 'MAJOR': 9, 'SPECIAL_NEEDS_INTEREST': 10,
     'APPLIED_T_LEADER': 12, 'IMPORTED_SCHEDULE_START': 14, 'IMPORTED_SCHEDULE_END': 47, 'LOCATION': 51}

# Volunteer Schedule Constants
# Each volunteer fills out a Google Form (individuals.csv) where they input their time commitments from
# Monday to Thursday. The schedule starts at 7:15 AM (SCHEDULE_START_TIME) and continues in 15 min blocks
# (SCHEDULE_BLOCK_LENGTH) for 34 (NUMBER_of_PERIODS_PER_DAYS) blocks until 3:45 PM

# duration of each time period in individuals.csv Google Form (minutes)
SCHEDULE_BLOCK_LENGTH = 15

# time that the schedule in the individuals.csv Google Form starts at (in military time)
SCHEDULE_START_TIME = 715

# number of periods of length SCHEDULE_BLOCK_LENGTH for each day that starts at SCHEDULE_START_TIME
NUMBER_OF_BLOCKS_PER_DAY = 34

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
