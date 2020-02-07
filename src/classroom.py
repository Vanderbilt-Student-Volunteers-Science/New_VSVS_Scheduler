import src.convertSchedule

#  SCHOOL TRAVEL TIME CONSTANTS (one-way, in minutes)
HEAD = 20
HILL = 25
OTHER = 45


class Classroom:
    def __init__(self, teacher_name, teacher_phone, school, teacher_email, class_start_time, class_end_time, day_of_week):
        self.teacher_name = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = teacher_email
        self.class_start_time = src.convertSchedule.convert_to_military(class_start_time)
        self.class_end_time = src.convertSchedule.convert_to_military(class_end_time)
        self.day_of_week = day_of_week
        self.volunteers_assigned = 0

        #  maybe a better way to do this? don't want to put if statements in both convertSchedule methods
        if self.school == 'Head':
            self.free_time_start = src.convertSchedule.calculate_free_time_start(self.class_start_time, HEAD)
            self.volunteer_time_needed = src.convertSchedule.calculate_free_time_needed(self.class_start_time, self.class_end_time, HEAD)
        elif self.school == 'H.G. Hill':
            self.free_time_start = src.convertSchedule.calculate_free_time_start(self.class_start_time, HILL)
            self.volunteer_time_needed = src.convertSchedule.calculate_free_time_needed(self.class_start_time, self.class_end_time, HILL)
        else:
            self.free_time_start = src.convertSchedule.calculate_free_time_start(self.class_start_time, OTHER)
            self.volunteer_time_needed = src.convertSchedule.calculate_free_time_needed(self.class_start_time, self.class_end_time, OTHER)

    def add_preassigned_volunteer(self):
        self.volunteers_assigned += 1
