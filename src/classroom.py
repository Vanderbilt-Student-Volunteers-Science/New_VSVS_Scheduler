import src.globalAttributes
import src.convertSchedule


class Classroom:

    def __init__(self, group_number, teacher_name, teacher_phone, school, teacher_email, class_start_time, class_end_time, day_of_week):
        self.group_number = group_number
        self.teacher_name = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = teacher_email
        self.class_start_time = src.convertSchedule.convert_to_military(class_start_time)
        self.class_end_time = src.convertSchedule.convert_to_military(class_end_time)
        self.day_of_week = day_of_week
        self.volunteers_assigned = 0
        self.t_leader = 0  # has a team leader?
        self.driver = 0  # has a driver?

        # the latest time a volunteer can start being available and be able to make it to the beginning of a lesson
        self.free_time_start = src.convertSchedule.calculate_free_time_start(self.class_start_time, src.globalAttributes.SCHOOL_TRAVEL_TIME)

        # free time needed starting at free_time_start for a volunteer to be able to make the end of the lesson
        self.volunteer_time_needed = src.convertSchedule.calculate_free_time_needed(self.class_start_time, self.class_end_time, src.globalAttributes.SCHOOL_TRAVEL_TIME)

        # the index in the array of the volunteer schedule that needs to be >= volunteer_time_needed for a volunteer to be able to visit this classroom
        self.start_time_schedule_index = src.convertSchedule.military_to_schedule_array(self.day_of_week, self.free_time_start)

    def assign_volunteer(self, volunteer):
        self.volunteers_assigned += 1
        volunteer.set_group_number(self.group_number)
        if self.driver == 0 and volunteer.driver:
            self.driver = 1
            volunteer.assign_driver()
        if self.t_leader == 0 and volunteer.applied_t_leader:
            self.t_leader = 1
            volunteer.assign_t_leader()