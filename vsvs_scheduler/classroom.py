from datetime import datetime, timedelta
from time import strftime
from teacher import Teacher


class Classroom:
    def __init__(self, group_number: int, teacher: Teacher, start_time: str, end_time: str, weekdays: []):
        """

        :param group_number:
        :param start_time:
        :param end_time:
        :param weekday:
        """
        self.group_number = group_number
        self.teacher = teacher
        self.weekdays = weekdays
        self.weekday_idx = 0
        self.weekday = weekdays[self.weekday_idx]
        self.volunteers = []
        self.possible_volunteers = 0
        self.possible_partner_groups = 0
        self.team_leader = False  # has a team leader?
        self.start_time = datetime.strptime(start_time, '%I:%M:%S %p')  # time the class starts in military time
        self.end_time = datetime.strptime(end_time, '%I:%M:%S %p')  # time the class ends in military time

    def assign_volunteer(self, volunteer):
        """
        Assigns a volunteer to a classroom. Updates the volunteer.group_number with the group number of the classroom.
        If the classroom doesn't have a team leader and the volunteer applied to be one, it sets the Classroom t_leader
        equal to this volunteer and updates volunteer.assigned_t_leader.

        :param volunteer:volunteer being assigned
        :return: None
        """
        self.volunteers.append(volunteer)
        volunteer.group_number = self.group_number
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assigned_leader = True

    def unassign_volunteers(self):
        for volunteer in self.volunteers:
            volunteer.group_number = -1
            volunteer.assigned_leader = False
            volunteer.possible_classrooms = 0
        self.volunteers = []
        self.team_leader = False

    def duration(self):
        """:returns: minutes of free time needed to perform a lesson, including driving and teaching time."""
        return (self.end_time - self.start_time + timedelta(hours=1)).seconds/60
    
    def change_to_next_preferred_day(self):
        possible_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        if self.weekday_idx < 3 and self.weekdays[self.weekday_idx + 1] in possible_weekdays:
            self.weekday_idx += 1
            self.weekday = self.weekdays[self.weekday_idx]

    def __repr__(self):
        return f"{self.teacher.name} at {self.teacher.school} on {self.weekday} ({self.start_time.strftime( '%I:%M %p')} - {strftime(self.end_time.strftime('%I:%M %p'))})\n"
