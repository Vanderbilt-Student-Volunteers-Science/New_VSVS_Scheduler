from datetime import datetime, timedelta
from time import strftime
from .teacher import Teacher


class Classroom:

    def __init__(self, group_number: int, teacher: Teacher, start_time: str, end_time: str, weekdays: []):
        """
        Classroom object that holds information about a classroom and its volunteers.

        group_number: group number of the classroom
        teacher: teacher object
        start_time: time the class starts
        end_time: time the class ends
        weekdays: list of weekdays the class is held on in order of preference
        """
        self.group_number = group_number
        self.teacher = teacher 

        self.weekdays = weekdays 
        self.weekday_idx = 0 # index of the weekday in weekdays
        self.weekday = weekdays[self.weekday_idx] # weekday the class is held on

        self.volunteers = [] 
        self.possible_volunteers = 0  
        self.possible_partner_groups = 0  
        self.team_leader = False  

        self.start_time = datetime.strptime(start_time, '%I:%M:%S %p')  
        self.end_time = datetime.strptime(end_time, '%I:%M:%S %p')  



    def assign_volunteer(self, volunteer):
        """ Assigns volunteer to the classroom and updates the volunteer's group number and assigned_leader status."""

        self.volunteers.append(volunteer)
        volunteer.group_number = self.group_number
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assigned_leader = True



    def unassign_volunteers(self):
        """ Unassigns volunteers from the classroom and resets their group number and assigned_leader status."""

        for volunteer in self.volunteers:
            volunteer.group_number = -1
            volunteer.assigned_leader = False
            volunteer.possible_classrooms = 0
        self.volunteers = []
        self.team_leader = False



    def duration(self):
        """ Returns the duration of the class in minutes. (includes travel time) """
        return (self.end_time - self.start_time + timedelta(hours=1)).seconds/60
    


    def change_to_next_preferred_day(self):
        """ Changes the weekday to the next preferred day."""
        
        possible_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        if self.weekday_idx < 3 and self.weekdays[self.weekday_idx + 1] in possible_weekdays:
            self.weekday_idx += 1
            self.weekday = self.weekdays[self.weekday_idx]



    def __repr__(self):
        return f"{self.teacher.name} at {self.teacher.school} on {self.weekday} ({self.start_time.strftime( '%I:%M %p')} - {strftime(self.end_time.strftime('%I:%M %p'))})\n"
