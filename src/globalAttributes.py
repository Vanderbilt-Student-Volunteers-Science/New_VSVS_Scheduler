# Contains global constants and variables for VSVS Volunteer Sorting Program


# CONSTANTS

# maximum number of volunteers to allow in a classroom group
MAX_TEAM_SIZE = 3

# minimum acceptable number of volunteers in a classroom group that can visit a classroom
MIN_TEAM_SIZE = 3

# minutes to travel one-way to any school
SCHOOL_TRAVEL_TIME = 45

# index for each field in the individuals csv
I = {'FIRST': 3, 'LAST': 4, 'PHONE': 5, 'EMAIL': 6, 'SCHOOL': 7, 'YEAR': 8, 'MAJOR': 9, 'SPECIAL_NEEDS_INTEREST': 10,
     'APPLIED_T_LEADER': 12, 'IMPORTED_SCHEDULE_START': 14, 'IMPORTED_SCHEDULE_END': 47, 'LOCATION': 51}

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
