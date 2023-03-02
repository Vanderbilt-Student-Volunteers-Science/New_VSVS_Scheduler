from datetime import datetime, timedelta


class Classroom:
    def __init__(self, group_number: int, name: str, phone: str, school: str, email: str,
                 start_time: str, end_time: str, weekday: str = "Monday"):
        """

        :param group_number:
        :param name:
        :param phone:
        :param school:
        :param email:
        :param start_time:
        :param end_time:
        :param weekday:
        """
        self.group_number = group_number
        self.teacher = name
        self.phone = phone
        self.school = school
        self.teacher_email = email
        self.weekday = weekday
        self.volunteers = []
        self.possible_volunteers = 0
        self.team_leader = False  # has a team leader?
        self.start_time = datetime.strptime(start_time, '%H:%M')  # time the class starts in military time
        self.end_time = datetime.strptime(end_time, '%H:%M')  # time the class ends in military time

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
        return (self.end_time - self.start_time + timedelta(minutes=30)).seconds / 60

    def __str__(self):
        return self.teacher + ' at ' + self.school
