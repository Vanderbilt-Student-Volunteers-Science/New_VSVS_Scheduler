import src.convert_schedule
import src.global_attributes
from src.volunteer import Volunteer


class Classroom:

    def __init__(self, group_number, teacher_name, teacher_phone, school, teacher_email, class_start_time,
                 class_end_time, day_of_week):
        """ Classroom constructor

        :param group_number: classroom number
        :type group_number: int
        :param teacher_name: teacher name
        :type teacher_name: str
        :param teacher_phone: teacher phone number
        :type teacher_phone: str
        :param school: school where classroom is
        :type school: str
        :param teacher_email: teacher email address
        :type teacher_email: str
        :param class_start_time: start time of lesson (eg. 1:00 PM)
        :type class_start_time: str
        :param class_end_time: end time of lesson (eg. 1:55 PM)
        :type class_end_time: str
        :param day_of_week: day of the week
        :type day_of_week: str
        """

        # TODO: make group_number the index of classroom in classroom_list
        self.group_number = group_number
        self.teacher_name = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = teacher_email
        self.day_of_week = day_of_week
        self.volunteers_assigned = 0

        # has a team leader?
        self.t_leader = False

        # time the class starts in military time
        self.class_start_time = src.convert_schedule.convert_to_military(class_start_time)

        # time the class ends in military time
        self.class_end_time = src.convert_schedule.convert_to_military(class_end_time)

        # the latest time a volunteer can start being available and be able to make this lesson
        self.free_time_start = src.convert_schedule.calculate_free_time_start(self.class_start_time,
                                                                              src.global_attributes.SCHOOL_TRAVEL_TIME)

        # minutes of free time needed starting at free_time_start for a volunteer to be able to make this lesson
        self.volunteer_time_needed = src.convert_schedule.calculate_free_time_needed(self.class_start_time,
                                                                                     self.class_end_time,
                                                                                     src.global_attributes.SCHOOL_TRAVEL_TIME)

        # the index in the array of Volunteer attribute free_time_array (or partner_schedule) that needs to be
        # >= volunteer_time_needed for a volunteer to be able to visit this classroom
        self.start_time_schedule_index = src.convert_schedule.military_to_free_time_array(self.day_of_week,
                                                                                          self.free_time_start)

        self.volunteers = []

    def assign_volunteer(self, volunteer):
        """ Assigns a volunteer to a classroom. Updates the Volunteer group_number attribute with the group number of
        the classroom the volunteer is being assigned to and the Classroom object with a new volunteers_assigned value.
        If the classroom doesn't have a team leader or driver and the volunteer is one of those, sets the Classroom
        t_leader and Volunteer assigned_t_leader attributes or the Classroom driver and Volunteer assigned_driver
        attributes.

        :param volunteer: volunteer being assigned to self Classroom object
        :type volunteer: Volunteer
        :return: None
        """
        if self.volunteers_assigned < src.global_attributes.MAX_TEAM_SIZE:
            self.volunteers_assigned += 1
            self.volunteers.append(volunteer)

            volunteer.group_number = self.group_number
            if not self.t_leader and volunteer.applied_t_leader:
                self.t_leader = True
                # assign volunteer as team leader
                volunteer.assigned_t_leader = True

    def empty_classroom(self):
        """unassigns volunteers from a classroom and returns a list of the volunteers that were unassigned

        :return: list of the volunteers that were unassigned
        :rtype: list[Volunteer]
        """
        unassigned_volunteers = []
        for volunteer in src.global_attributes.volunteer_list:
            if volunteer.group_number == self.group_number:
                # unassign volunteers
                volunteer.set_group_number(-1)
                volunteer.assigned_t_leader = False
                volunteer.assigned_driver = False
                unassigned_volunteers.append(volunteer)

        # make classroom empty
        self.volunteers_assigned = 0
        self.t_leader = False
        self.volunteers = []
        return unassigned_volunteers

    def __str__(self):
        return self.teacher_name + ' @ ' + self.school

