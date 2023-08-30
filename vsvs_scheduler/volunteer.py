from datetime import timedelta
from classroom import Classroom
from schedule import Schedule


class Volunteer:

    def __init__(self, first: str, last: str, phone: str, email: str, schedule: Schedule, leader_app: bool = False, 
                 robotics_interest: bool = False, special_needs_interest: bool = False, board_member: bool = False):
        
        self.first = first.capitalize()
        self.last = last.capitalize()
        self.phone = phone
        self.email = email.lower() #USE REGEX
        self.board = board_member

        self.leader_app = leader_app or board_member  # if volunteer applied to be a team leader or is board member

        self.availability = schedule
        self.group_number = -1  # -1 means unassigned
        self.assigned_leader = False  # Was the volunteer assigned to be their group's team leader?
        self.possible_classrooms = 0  # number of classrooms the volunteer can make


    def can_make_class(self, classroom: Classroom):
        """Returns boolean of whether volunteer/partner group can make a classroom based on the schedule parameter.

        :param classroom:
        :param volunteers:
        :return: bool: whether volunteer/partners can make that class
        """
        time_deviation = classroom.start_time.minute % 15
        if time_deviation != 0:
            new_time = classroom.start_time - timedelta(minutes=time_deviation)
            time = new_time
        else:
            time = classroom.start_time
        time = time - timedelta(minutes=30)

        weekday_schedule = self.availability.find_day_availability(classroom.weekday)
        if time in weekday_schedule:
            return weekday_schedule[time] >= classroom.duration()

        return False
    
    def assign_classroom(self, classroom: Classroom):
        self.group_number = classroom.group_number
    
    def __str__(self):
        return f"{self.first} {self.last}"


        