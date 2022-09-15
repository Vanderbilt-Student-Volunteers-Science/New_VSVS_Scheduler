import src.convertSchedule
from __init__ import volunteer_list, SCHOOL_TRAVEL_TIME


class Classroom:

    def __init__(self, group_number: int, teacher_name: str, teacher_phone: str, school: str, teacher_email: str,
                 class_start_time: str, class_end_time: str, day_of_week: str):

        # TODO: make group_number the index of classroom in classroom_list
        self.group_number = group_number
        self.teacher = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = teacher_email
        self.day_of_week = day_of_week
        self.volunteers_assigned = 0

        # has a team leader?
        self.team_leader = False

        # time the class starts in military time
        self.start_time = src.convertSchedule.convert_to_military(class_start_time)

        # time the class ends in military time
        self.end_time = src.convertSchedule.convert_to_military(class_end_time)

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

    # Assigns a volunteer to a classroom. Updates the Volunteer group_number attribute with the group number of the
    # classroom the volunteer is being assigned to and the Classroom object with a new volunteers_assigned value. If
    # the classroom doesn't have a team leader or driver and the volunteer is one of those, sets the Classroom t_leader
    # and Volunteer assigned_t_leader attributes or the Classroom driver and Volunteer assigned_driver attributes.
    # self -      Classroom object volunteer is being assigned to
    # volunteer - volunteer being assigned to self Classroom object
    def assign_volunteer(self, volunteer):
        self.volunteers_assigned += 1
        volunteer.set_group_number(self.group_number)
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.assign_t_leader()

    # unassigns volunteers from a classroom and returns a list of the volunteers that were unassigned
    def empty_classroom(self):
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
