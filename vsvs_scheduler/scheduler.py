import warnings
from datetime import datetime
from applicants.classroom import Classroom
from applicants.volunteer import Volunteer
from applicants.partners import Partners
from data_uploader import DataUploader
from __init__ import MAX_TEAM_SIZE, MIN_TEAM_SIZE, EARLIEST_TIME, LATEST_TIME



class Scheduler:
    def __init__(self):
        """Scheduler object that holds information about the schedule and the volunteers and classrooms."""

        self.earliest_time = datetime.strptime(EARLIEST_TIME, "%H:%M")
        self.latest_time = datetime.strptime(LATEST_TIME, "%H:%M")

        data = DataUploader()
        self.volunteers: list[Volunteer] = data.volunteers
        self.classrooms: list[Classroom] = data.classrooms
        self.partners: list[Partners] = data.partners

        self.unassigned_partners = []
        self.incomplete_classrooms = self.classrooms.copy()



    def create_assignments(self):
        
        self.unassigned_partners = self.assign_partners()
        
        self.assign_volunteers("board")
        self.assign_volunteers("leaders")
        self.assign_volunteers()

        missing_team_leaders = [classroom for classroom in self.classrooms if not classroom.team_leader]

        num_days_to_try = 4

        while num_days_to_try > 0 and self.incomplete_classrooms:
            updated_teachers = []
            for classroom in self.incomplete_classrooms:
                classroom.unassign_volunteers()
                if classroom.teacher not in updated_teachers:
                    classroom.change_to_next_preferred_day()
                    updated_teachers.append(classroom.teacher)
            self.assign_volunteers()
            num_days_to_try -= 1
        
        num_days_to_try = 4
        updated_teachers = []
        for classroom in self.incomplete_classrooms:
            if classroom.teacher not in updated_teachers:
                classroom.teacher.reset_weekday()
                updated_teachers.append(classroom.teacher)

        while num_days_to_try > 0 and self.incomplete_classrooms:
            updated_teachers = []
            for classroom in self.incomplete_classrooms:
                classroom.unassign_volunteers()
                if classroom.teacher not in updated_teachers:
                    classroom.change_to_next_preferred_day()
                    updated_teachers.append(classroom.teacher)
            self.assign_volunteers("second_to_last_round")
            num_days_to_try -= 1

        self.assign_volunteers("last_round")
        for classroom in self.classrooms:
            classroom.freeze_weekday()

        if missing_team_leaders:
            warnings.warn(f'WARNING: Classrooms are missing team leaders: {missing_team_leaders}\n')
        if self.incomplete_classrooms:
            warnings.warn(f'WARNING: Classrooms without necessary number of volunteers {self.incomplete_classrooms}\n')
        return {"unassigned": self.unassigned_partners}
    
    def assign_partners(self):
        """Assigns partners to classrooms and returns a list of unassigned partners."""

        self.find_possible_classroom_and_partners_matches()
        idx = 0
        unassigned_groups = []
        for group in self.partners:
            while group.group_number == -1 and idx < len(self.incomplete_classrooms):
                curr_class = self.incomplete_classrooms[idx]
                if group.can_make_class(curr_class, MAX_TEAM_SIZE):
                    group.assign_partners(curr_class)
                    if len(curr_class.volunteers) >= MAX_TEAM_SIZE:
                        self.incomplete_classrooms.remove(curr_class)
                else:
                    idx += 1
            if group.group_number == -1:
                unassigned_groups.append(group)

        return unassigned_groups
    


    def assign_volunteers(self, volunteer_type: str = "default"):
        """Assigns volunteers to classrooms based on the volunteer_type parameter."""

        self.find_possible_classroom_and_volunteer_matches()

        volunteer_list = self.volunteers
        
        if volunteer_type == "leaders":
            volunteer_list = [volunteer for volunteer in self.volunteers if volunteer.leader_app]
        elif volunteer_type == "board":
            volunteer_list = [volunteer for volunteer in self.volunteers if volunteer.board]
        
        if volunteer_type == "last_round":
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.classrooms):
                    classroom = self.classrooms[idx]
                    if volunteer.can_make_class_last_round(classroom) and (len(classroom.volunteers) < MAX_TEAM_SIZE):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)
                    else:
                        idx += 1
        elif volunteer_type == "second_to_last_round":
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                    classroom = self.incomplete_classrooms[idx]
                    if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)
                        if len(classroom.volunteers) >= MIN_TEAM_SIZE:
                            self.incomplete_classrooms.remove(classroom)
                            classroom.freeze_weekday()
                    else:
                        idx += 1
        else:
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                    classroom = self.incomplete_classrooms[idx]
                    if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)
                        if len(classroom.volunteers) >= MIN_TEAM_SIZE:
                            self.incomplete_classrooms.remove(classroom)
                    else:
                        idx += 1
            self.unassign_volunteers_for_incomplete_classes()

        self.incomplete_classrooms.sort(key=lambda classroom: len(classroom.volunteers), reverse=True)

    
    def unassign_volunteers_for_incomplete_classes(self):
        for classroom in self.incomplete_classrooms:
            classroom.teacher.unassign_volunteers()
            for room in classroom.teacher.classrooms:
                if room not in self.incomplete_classrooms:
                    self.incomplete_classrooms.append(room)


    def find_possible_classroom_and_partners_matches(self):
        """Finds the number of possible classrooms each partner group can make and the number of possible partner groups each classroom can have."""

        for group in self.partners:
            for classroom in self.incomplete_classrooms:
                if group.can_make_class(classroom, MAX_TEAM_SIZE):
                    group.increment_possible_classrooms()
                    classroom.possible_partner_groups += 1
        self.partners.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_partner_groups)


        
    def find_possible_classroom_and_volunteer_matches(self):
        """Finds the number of possible classrooms each volunteer can make and the number of possible volunteers each classroom can have."""
        for volunteer in self.volunteers:
            for classroom in self.incomplete_classrooms:
                if volunteer.group_number == -1 and volunteer.can_make_class(classroom):
                    volunteer.possible_classrooms += 1
                    classroom.possible_volunteers += 1
        self.volunteers.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_volunteers)

        

