import src.convertSchedule


class Classroom:
    def __init__(self, teacher_name, teacher_phone, school, teacher_email, start_time, end_time, day_of_week):
        self.teacher_name = teacher_name
        self.teacher_phone = teacher_phone
        self.school = school
        self.teacher_email = teacher_email
        self.start_time = src.convertSchedule.convert_to_military(start_time)
        self.end_time = src.convertSchedule.convert_to_military(end_time)
        self.day_of_week = day_of_week
        self.volunteers_assigned = 0

    def add_preassigned_volunteer(self):
        self.volunteers_assigned = self.volunteers_assigned + 1
