from classroom import Classroom
from schedule import Schedule


class Volunteer:
    """
    The Volunteer class represents a volunteer. 
    It holds information about the volunteer, their availability, and the classroom they are assigned to.
    """

    def __init__(self, first: str, last: str, phone: str, email: str, schedule: Schedule, leader_app: bool = False, 
                 robotics_interest: bool = False, special_needs_interest: bool = False, board_member: bool = False):
        """
        Initializes a Volunteer object with the given first name, last name, phone number, email, schedule, 
        leader application status, robotics interest, special needs interest, and board member status.

        Parameters:
        first (str): The first name of the volunteer.
        last  (str): The last name of the volunteer.
        phone (str): The phone number of the volunteer.
        email (str): The email address of the volunteer.
        schedule (Schedule): The schedule of the volunteer.
        leader_app (bool): Whether the volunteer applied to be a team leader.
        robotics_interest (bool): Whether the volunteer is interested in robotics.
        special_needs_interest (bool): Whether the volunteer is interested in special needs.
        board_member (bool): Whether the volunteer is a board member.
        """
        self.first = first.capitalize()
        self.last = last.capitalize()
        self.phone = phone         # TODO: Validate with regex
        self.email = email.lower() # TODO: Validate with regex
        self.board = board_member

        # if volunteer applied to be a team leader or is board member
        self.leader_app = leader_app or board_member  


        self.availability = schedule
        self.group_number = -1        # -1 means unassigned
        self.assigned_leader = False  # Was the volunteer assigned to be their group's team leader?
        self.possible_classrooms = 0  # number of classrooms the volunteer can make



    def can_make_class(self, classroom: Classroom):
        """
        Returns whether the volunteer can make a classroom based on the schedule parameter.

        Parameters:
        classroom (Classroom): The classroom to check.

        Returns:
        bool: True if the volunteer can make the classroom, False otherwise.
        """

        return self.availability.can_make_class(classroom)
    
    def can_make_class_last_round(self, classroom: Classroom):
        """
        Returns whether the volunteer can make a classroom based on the schedule parameter in the last round.

        Parameters:
        classroom (Classroom): The classroom to check.

        Returns:
        bool: True if the volunteer can make the classroom in the last round, False otherwise.
        """

        return self.availability.can_make_class(classroom, last_round=True)

    def assign_classroom(self, classroom: Classroom):
        """
        Assigns the volunteer to the classroom and updates the volunteer's group number.

        Parameters:
        classroom (Classroom): The classroom to assign.
        """

        self.group_number = classroom.group_number


        
    def __repr__(self):
        """
        Returns a string representation of the Volunteer object.

        Returns:
        str: A string representation of the Volunteer object.
        """
        return f"{self.first} {self.last}"


        