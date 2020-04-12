import src.globalAttributes
import src.convertSchedule


class Classroom:

    def __init__(self, group_number, teacher_name, teacher_phone, school, teacher_email, class_start_time, class_end_time, day_of_week):
        self.group_number = group_number
        self.teacher_name = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = teacher_email
        self.day_of_week = day_of_week
        self.volunteers_assigned = 0

        # has a team leader?
        self.t_leader = 0

        # has a driver?
        self.driver = 0

        # time the class starts in military time
        self.class_start_time = src.convertSchedule.convert_to_military(class_start_time)

        # time the class ends in military time
        self.class_end_time = src.convertSchedule.convert_to_military(class_end_time)

        # the latest time a volunteer can start being available and be able to make this lesson
        self.free_time_start = src.convertSchedule.calculate_free_time_start(self.class_start_time, src.globalAttributes.SCHOOL_TRAVEL_TIME)

        # minutes of free time needed starting at free_time_start for a volunteer to be able to make this lesson
        self.volunteer_time_needed = src.convertSchedule.calculate_free_time_needed(self.class_start_time, self.class_end_time, src.globalAttributes.SCHOOL_TRAVEL_TIME)

        # the index in the array of Volunteer attribute free_time_array (or partner_schedule) that needs to be
        # >= volunteer_time_needed for a volunteer to be able to visit this classroom
        self.start_time_schedule_index = src.convertSchedule.military_to_free_time_array(self.day_of_week, self.free_time_start)

    # Assigns a volunteer to a classroom. Updates the Volunteer group_number attribute with the group number of the
    # classroom the volunteer is being assigned to and the Classroom object with a new volunteers_assigned value. If
    # the classroom doesn't have a team leader or driver and the volunteer is one of those, sets the Classroom t_leader
    # and Volunteer assigned_t_leader attributes or the Classroom driver and Volunteer assigned_driver attributes.
    # self -      Classroom object volunteer is being assigned to
    # volunteer - volunteer being assigned to self Classroom object
    def assign_volunteer(self, volunteer):
        self.volunteers_assigned += 1
        volunteer.set_group_number(self.group_number)
        if self.driver == 0 and volunteer.driver:
            self.driver = 1
            volunteer.assign_driver()
        if self.t_leader == 0 and volunteer.applied_t_leader:
            self.t_leader = 1
            volunteer.assign_t_leader()
