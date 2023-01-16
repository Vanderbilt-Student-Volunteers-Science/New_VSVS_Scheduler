from datetime import datetime, timedelta


# Classroom
# This is Cal adding a comment to see if he can get the Superlinter to work

class Classroom:
    """
    This class stores classroom information
    """

    def __init__(self, group_number: int, name: str, phone: str, school: str, email: str,
                 start_time: str, end_time: str):
        """
        :param group_number:
        :param teacher_name:
        :param teacher_phone:
        :param school:
        :param email: teacher's email address
        :param start_time: time at which the class starts
        :param end_time: time at which the class ends
        :param day: day of the week for that class
        """

        # TODO: make group_number the index of classroom in classroom_list
        self.group_number = group_number
        self.teacher = name
        self.phone = phone
        self.school = school
        self.teacher_email = email
        self.weekday = "Monday"
        self.num_of_volunteers = 0

        # has a team leader?
        self.team_leader = False

        # time the class starts in military time
        self.start_time = datetime.strptime(start_time, '%H:%M:%S %p')

        # time the class ends in military time
        self.end_time = datetime.strptime(end_time, '%H:%M:%S %p')

        # the latest time a volunteer can start being available and be able to make this lesson
        self.free_time_start = self.start_time - timedelta(minutes=30)

        # minutes of free time needed starting at free_time_start for a volunteer to be able to make this lesson
        self.volunteer_time_needed = (self.end_time - self.start_time) + timedelta(minutes=30)

    def assign_volunteer(self, volunteer):
        """
        Assigns a volunteer to a classroom. Updates the volunteer.group_number with the group number of the classroom.
        If the classroom doesn't have a team leader and the volunteer applied to be one, it sets the Classroom t_leader
        equal to this volunteer and updates volunteer.assigned_t_leader.

        :param volunteer:volunteer being assigned
        :return: None
        """
        self.num_of_volunteers += 1
        volunteer.group_number = self.group_number
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assigned_leader = True

    def empty_classroom(self):
        """Unassigns all volunteers from a classroom

        :return: list of the volunteers that were unassigned
        """
        unassigned_volunteers = []
        for volunteer in volunteer_list:
            if volunteer.group_number == self.group_number:
                # unassign volunteers
                volunteer.group_number = -1
                volunteer.assigned_leader = False
                unassigned_volunteers.append(volunteer)

        # make classroom empty
        self.num_of_volunteers = 0
        self.team_leader = False
        return unassigned_volunteers

    def free_time_duration(self):
        """:returns: minutes of free time needed to perform a lesson, including driving and teaching time."""
        return (self.end_time - self.start_time + timedelta(minutes=30)).seconds/60

    def __str__(self):
        return self.teacher + ' at ' + self.school
