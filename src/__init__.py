# Global variables
volunteer_list = []  # contains all the Volunteer objects, one for each VSVS volunteer
classroom_list = []  # contains all the Classroom objects, one for each VSVS group that needs to be created
partially_filled_classrooms = []  # contains all Classroom objects that are partially filled
empty_classrooms = []  # contains all Classroom objects that are empty

SCHOOL_TRAVEL_TIME = 15  # minutes to travel one-way to any school
MAX_TEAM_SIZE = 4  # maximum number of volunteers to allow in a classroom group
MIN_TEAM_SIZE = 3  # minimum acceptable number of volunteers in a classroom group that can visit a classroom
