from .classroom import Classroom
from .schedule import Schedule


class Volunteer:

    def __init__(self, first: str, last: str, phone: str, email: str, schedule: Schedule, leader_app: bool = False, 
                 robotics_interest: bool = False, special_needs_interest: bool = False, board_member: bool = False):
        """ Volunteer object that holds information about a volunteer and their schedule.

        first: first name of the volunteer
        last: last name of the volunteer
        phone: phone number of the volunteer
        email: email of the volunteer
        schedule: schedule object of the volunteer
        leader_app: boolean of whether the volunteer applied to be a team leader
        robotics_interest: boolean of whether the volunteer is interested in robotics
        special_needs_interest: boolean of whether the volunteer is interested in special needs
        board_member: boolean of whether the volunteer is a board member
        """
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
        """Returns boolean of whether volunteer can make a classroom based on the schedule parameter."""

        return self.availability.can_make_class(classroom)
    


    def assign_classroom(self, classroom: Classroom):
        """Assigns the volunteer to the classroom and updates the volunteer's group number."""

        self.group_number = classroom.group_number


        
    def __repr__(self):
        return f"{self.first} {self.last}"


        