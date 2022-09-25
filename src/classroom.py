import src.convertSchedule
from __init__ import volunteer_list, SCHOOL_TRAVEL_TIME


class Classroom:
    """
    This class stores classroom information: group number, teacher name, teacher phone, school, teacher's email, class
     start time, class end time, day of the week """

    def __init__(self, group_number: int, teacher_name: str, teacher_phone: str, school: str, email: str,
                 start_time: str, end_time: str, day: str):
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
        self.teacher = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = email
        self.day_of_week = day
        self.volunteers_assigned = 0

        # has a team leader?
        self.team_leader = False

        # time the class starts in military time
        self.start_time = src.convertSchedule.convert_to_military(start_time)

        # time the class ends in military time
        self.end_time = src.convertSchedule.convert_to_military(end_time)

        # the latest time a volunteer can start being available and be able to make this lesson
        self.free_time_start = src.convertSchedule.calculate_free_time_start(self.start_time, SCHOOL_TRAVEL_TIME)

        # minutes of free time needed starting at free_time_start for a volunteer to be able to make this lesson
        self.volunteer_time_needed = src.convertSchedule.calculate_free_time_needed(self.start_time,
                                                                                    self.end_time,
                                                                                    SCHOOL_TRAVEL_TIME)

        # the index in the array of Volunteer attribute free_time_array (or partner_schedule) that needs to be
        # >= volunteer_time_needed for a volunteer to be able to visit this classroom
        self.start_time_schedule_index = src.convertSchedule.military_to_free_time_array(self.day_of_week,
                                                                                         self.free_time_start)

    def assign_volunteer(self, volunteer):
        """
        Assigns a volunteer to a classroom. Updates the volunteer.group_number with the group number of the classroom.
        If the classroom doesn't have a team leader and the volunteer applied to be one, it sets the Classroom t_leader
        equal to this volunteer and updates volunteer.assigned_t_leader.

        :param volunteer:volunteer being assigned
        :return: None
        """
        self.volunteers_assigned += 1
        volunteer.set_group_number(self.group_number)
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assign_t_leader()

    def empty_classroom(self):
        """Unassigns all volunteers from a classroom

        :return: list of the volunteers that were unassigned
        """
        unassigned_volunteers = []
        for volunteer in volunteer_list:
            if volunteer.group_number == self.group_number:
                # unassign volunteers
                volunteer.set_group_number(-1)
                volunteer.assigned_t_leader = False
                unassigned_volunteers.append(volunteer)

        # make classroom empty
        self.volunteers_assigned = 0
        self.team_leader = False
        return unassigned_volunteers

    def __str__(self):
        return self.teacher + ' at ' + self.school
