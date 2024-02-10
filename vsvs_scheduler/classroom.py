from datetime import datetime, timedelta
from time import strftime
from teacher import Teacher
from globals import TRAVEL_TIME_HOURS


class Classroom:
    """
    The Classroom class represents a class and holds information about the classroom, the teacher, the 
    class timings, and the volunteers assigned to the classroom.
    """

    def __init__(self, group_number: int, teacher: Teacher, start_time: str, end_time: str):
        """
        Initializes a Classroom object with the given group number, teacher, start time, and end time.

        Parameters:
        group_number (int): The group number of the classroom.
        teacher (Teacher): The teacher of the classroom.
        start_time (str): The start time of the class.
        end_time (str): The end time of the class.
        """
        self.group_number = group_number
        self.teacher = teacher 

        self.volunteers = [] # List to hold the volunteers assigned to the classroom
        self.possible_volunteers = 0  # Counter for possible volunteers
        self.possible_partner_groups = 0 # Counter for possible partner groups
        self.team_leader = False # Flag to indicate if a team leader is assigned
        self.weekday = None # The weekday when the class is held

        # Convert the start and end times from string to datetime objects
        self.start_time = datetime.strptime(start_time, '%I:%M:%S %p') 
        self.end_time = datetime.strptime(end_time, '%I:%M:%S %p')  



    def assign_volunteer(self, volunteer):
        """
        Assigns a volunteer to the classroom and updates the volunteer's group number and assigned_leader status.

        Parameters:
        volunteer (Volunteer): The volunteer to be assigned.
        """

        self.volunteers.append(volunteer)
        volunteer.group_number = self.group_number
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assigned_leader = True



    def unassign_volunteers(self):
        """
        Unassigns all volunteers from the classroom and resets their group number and assigned_leader status.
        """

        for volunteer in self.volunteers:
            volunteer.group_number = -1
            volunteer.assigned_leader = False
            volunteer.possible_classrooms = 0
        self.volunteers = []
        self.team_leader = False

    def change_to_next_preferred_day(self):
        """ 
        Updates the weekday to the next weekday preference. 
        """

        self.teacher.next_weekday()
    
    def freeze_weekday(self):
        """ 
        Freezes the weekday to the current weekday preference. 
        """
        if self.weekday is None:
            self.weekday = self.teacher.weekday

    def duration(self):
        """
        Returns the duration of the class in minutes. (includes travel time)

        Returns:
        int: The duration of the class in minutes.
        """
        return (self.end_time - self.start_time + timedelta(hours=TRAVEL_TIME_HOURS)).seconds/60
    

    def __repr__(self):
        """
        Returns a string representation of the Classroom object.

        Returns:
        str: A string representation of the Classroom object.
        """
        return f"{self.teacher.name} at {self.teacher.school} on {self.teacher.weekday} ({self.start_time.strftime( '%I:%M %p')} - {strftime(self.end_time.strftime('%I:%M %p'))})\n"
