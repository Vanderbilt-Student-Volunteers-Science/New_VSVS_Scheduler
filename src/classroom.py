from datetime import datetime, timedelta

import src.convertSchedule


class Classroom():
    """This class is derived from the Applicant class and stores classroom information"""

    def __init__(self, teacher: str, phone: str, email: str, group_number: int, school: str, start_time: str,
                 end_time: str):
        """

        :param name:
        :param phone:
        :param email:
        :param group_number:
        :param school:
        :param start_time:time at which the class starts
        :param end_time:time at which the class ends
        """
        self.teacher = teacher
        self.phone = phone
        self.email = email
        self.group_number = group_number
        self.number_of_volunteers = 0
        self.school = school
        self.weekday = "Monday"
        self.team_leader = False  # has a team leader?

        # time the class starts/ends in military time
        self.start_time = datetime.strptime(start_time, '%I:%M:%S %p')
        self.end_time = datetime.strptime(end_time, '%I:%M:%S %p')

        # TODO: make group_number the index of classroom in classroom_list

        # the latest time a volunteer can start being available and be able to make this lesson
#        self.free_time_start = src.convertSchedule.calculate_free_time_start(self.start_time, 15)

        # the index in the array of Volunteer attribute free_time_array (or partner_schedule) that needs to be
        # >= volunteer_time_needed for a volunteer to be able to visit this classroom
        #self.start_time_schedule_index = src.convertSchedule.military_to_free_time_array(self.weekday,
        #                                                                                 self.free_time_start)

    def free_time_needed(self):
        """Returns minutes of free time needed to perform a lesson, including driving and teaching time.
        :returns: minutes of free time needed starting at free_time_start for a volunteer to attend the lesson """
        return (self.end_time - self.start_time + timedelta(minutes=15)).total_seconds()/60

    def assign_volunteer(self, volunteer):
        """
        Assigns a volunteer to a classroom. Updates the volunteer.group_number with the group number of the classroom.
        If the classroom doesn't have a team leader and the volunteer applied to be one, it sets the Classroom t_leader
        equal to this volunteer and updates volunteer.assigned_t_leader.

        :param volunteer:volunteer being assigned
        :return: None
        """
        self.number_of_volunteers += 1
        volunteer.set_group_number(self.group_number)
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assign_t_leader()

    # def empty_classroom(self):
    #     """Unassigns all volunteers from a classroom
    #
    #     :return: list of the volunteers that were unassigned
    #     """
    #     unassigned_volunteers = []
    #     for volunteer in volunteer_list:
    #         if volunteer.group_number == self.group_number:
    #             # unassign volunteers
    #             volunteer.set_group_number(-1)
    #             volunteer.assigned_t_leader = False
    #             unassigned_volunteers.append(volunteer)
    #
    #     # make classroom empty
    #     self.number_of_volunteers = 0
    #     self.team_leader = False
    #     return unassigned_volunteers

    def __str__(self):
        return self.name + ' at ' + self.school
