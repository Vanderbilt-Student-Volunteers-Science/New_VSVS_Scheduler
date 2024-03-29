import warnings
from datetime import datetime
from applicants.classroom import Classroom
from applicants.volunteer import Volunteer
from applicants.partners import Partners
from volunteer_data_uploader import VolunteerDataUploader
from class_data_uploader import ClassDataUploader
from partner_data_uploader import PartnerDataUploader


class Scheduler:
    def __init__(self, earliest: str = "7:15", latest: str = "15:30", max_team_size: int = 5, min_team_size: int = 3):
        """Scheduler object that holds information about the schedule and the volunteers and classrooms."""

        self.earliest_time = datetime.strptime(earliest, "%H:%M")
        self.latest_time = datetime.strptime(latest, "%H:%M")

        self.individuals: list[Volunteer] = VolunteerDataUploader().applicants
        self.classrooms: list[Classroom] = ClassDataUploader().applicants
        self.partners: list[Partners] = PartnerDataUploader(self.individuals).applicants

        self.unassigned_partners = []
        self.incomplete_classrooms = self.classrooms.copy()
        self.max_size = max_team_size
        self.min_size = min_team_size



    def create_assignments(self):
        
        self.unassigned_partners = self.assign_partners()
        
        self.assign_volunteers("board")
        self.assign_volunteers("leaders")
        self.assign_volunteers()

        missing_team_leaders = [classroom for classroom in self.classrooms if not classroom.team_leader]

        num_days_to_try = 4

        while num_days_to_try > 0 and self.incomplete_classrooms:
            for classroom in self.incomplete_classrooms:
                classroom.unassign_volunteers()
                classroom.change_to_next_preferred_day()
                self.assign_volunteers()
            num_days_to_try -= 1
        
        self.assign_volunteers("last_round")

        if missing_team_leaders:
            warnings.warn(f'WARNING: Classrooms are missing team leaders: {missing_team_leaders}')
        if self.incomplete_classrooms:
            warnings.warn(f'WARNING: Classrooms without necessary number of volunteers {self.incomplete_classrooms}')
        return {"unassigned": self.unassigned_partners}
    


    def assign_partners(self):
        """Assigns partners to classrooms and returns a list of unassigned partners."""

        self.find_possible_classroom_and_partners_matches()
        idx = 0
        unassigned_groups = []
        for group in self.partners:
            while group.group_number == -1 and idx < len(self.incomplete_classrooms):
                curr_class = self.incomplete_classrooms[idx]
                if group.can_make_class(curr_class, self.max_size):
                    group.assign_partners(curr_class)
                    if len(curr_class.volunteers) >= self.max_size:
                        self.incomplete_classrooms.remove(curr_class)
                else:
                    idx += 1
            if group.group_number == -1:
                unassigned_groups.append(group)

        return unassigned_groups
    


    def assign_volunteers(self, volunteer_type: str = "default"):
        """Assigns volunteers to classrooms based on the volunteer_type parameter."""

        self.find_possible_classroom_and_volunteer_matches()

        volunteer_list = self.individuals
        
        if volunteer_type == "leaders":
            volunteer_list = [volunteer for volunteer in self.individuals if volunteer.leader_app]
        elif volunteer_type == "board":
            volunteer_list = [volunteer for volunteer in self.individuals if volunteer.board]
        
        if volunteer_type == "last_round":
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.classrooms):
                    classroom = self.classrooms[idx]
                    if volunteer.can_make_class(classroom) and (len(classroom.volunteers) < self.max_size):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)
                    else:
                        idx += 1


        for volunteer in volunteer_list:
            idx = 0
            while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                classroom = self.incomplete_classrooms[idx]
                if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                    classroom.assign_volunteer(volunteer)
                    volunteer.assign_classroom(classroom)
                    if len(classroom.volunteers) >= self.min_size:
                        self.incomplete_classrooms.remove(classroom)
                else:
                    idx += 1
        self.incomplete_classrooms.sort(key=lambda classroom: len(classroom.volunteers), reverse=True)



    def find_possible_classroom_and_partners_matches(self):
        """Finds the number of possible classrooms each partner group can make and the number of possible partner groups each classroom can have."""

        for group in self.partners:
            for classroom in self.incomplete_classrooms:
                if group.can_make_class(classroom, self.max_size):
                    group.increment_possible_classrooms()
                    classroom.possible_partner_groups += 1
        self.partners.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_partner_groups)


        
    def find_possible_classroom_and_volunteer_matches(self):
        """Finds the number of possible classrooms each volunteer can make and the number of possible volunteers each classroom can have."""
        for volunteer in self.individuals:
            for classroom in self.incomplete_classrooms:
                if volunteer.group_number == -1 and volunteer.can_make_class(classroom):
                    volunteer.possible_classrooms += 1
                    classroom.possible_volunteers += 1
        self.individuals.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_volunteers)

        

