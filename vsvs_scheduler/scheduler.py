import csv
import os
import warnings
from datetime import datetime, timedelta

from classroom import Classroom
from volunteer import Volunteer
from partners import Partners
from data_uploader import VolunteerDataUploader, ClassDataUploader, PartnerDataUploader



class Scheduler:
    def __init__(self, earliest: str = "7:15", latest: str = "15:30", max_team_size: int = 4):
        self.earliest_time = datetime.strptime(earliest, "%H:%M")
        self.latest_time = datetime.strptime(latest, "%H:%M")

        self.individuals: list[Volunteer] = VolunteerDataUploader().applicants
        self.classrooms: list[Classroom] = ClassDataUploader().applicants
        self.partners: list[Partners] = PartnerDataUploader(self.individuals).applicants

        self.unassigned_partners = []
        self.incomplete_classrooms = self.classrooms.copy()
        self.max_size = max_team_size


    def create_assignments(self):

        self.unassigned_partners = self.assign_partners()
        
        self.assign_volunteers("board")
        self.assign_volunteers("leaders")
        self.assign_volunteers()

        missing_team_leaders = [classroom for classroom in self.classrooms if not classroom.team_leader]

        for classroom in self.incomplete_classrooms:
            classroom.unassign_volunteers()

        self.assign_volunteers()

        if missing_team_leaders:
            warnings.warn(f'WARNING: Classrooms are missing team leaders: {missing_team_leaders}')
        if self.incomplete_classrooms:
            warnings.warn(f'WARNING: Classrooms without necessary number of volunteers {incomplete_group}')
        return {"unassigned": self.unassigned_partners}

    def assign_partners(self):
        """
        Assigns a group of partners to a classroom they all can make (if there is one) using partner1.partner_schedule.
        When a group is assigned, uses classroom.assign_volunteer() for each partner (including partner1).

        :return:
        """
        self.find_possible_classroom_and_partners_matches()
        idx = 0
        unassigned_groups = []
        for group in self.partners:
            while group.group_number == -1 and idx < len(self.incomplete_classrooms):
                curr_class = self.incomplete_classrooms[idx]
                if group.can_make_class(curr_class):
                    group.assign_partners(curr_class)
                    if len(curr_class.volunteers) >= self.max_size:
                        self.incomplete_classrooms.remove(curr_class)
                else:
                    idx += 1
            if group.group_number == -1:
                unassigned_groups.append(group)

        return unassigned_groups

    def assign_volunteers(self, volunteer_type: str = "default"):
        self.find_possible_classroom_and_volunteer_matches()

        volunteer_list = self.individuals
        
        if volunteer_type == "leaders":
            volunteer_list = [volunteer for volunteer in self.individuals if volunteer.leader_app]
        elif volunteer_type == "board":
            volunteer_list = [volunteer for volunteer in self.individuals if volunteer.board]

        for volunteer in volunteer_list:
            idx = 0
            while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                classroom = self.incomplete_classrooms[idx]
                if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                    classroom.assign_volunteer(volunteer)
                    volunteer.assign_classroom(classroom)
                    if len(classroom.volunteers) >= self.max_size:
                        self.incomplete_classrooms.remove(classroom)
                else:
                    idx += 1
        self.incomplete_classrooms.sort(key=lambda classroom: len(classroom.volunteers))

    def find_possible_classroom_and_partners_matches(self):
        for group in self.partners:
            for classroom in self.incomplete_classrooms:
                if group.can_make_class(classroom):
                    group.increment_possible_classrooms()
                    classroom.possible_partner_groups += 1
        self.partners.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_partner_groups)

    def find_possible_classroom_and_volunteer_matches(self):
        for volunteer in self.individuals:
            for classroom in self.incomplete_classrooms:
                if volunteer.group_number == -1 and volunteer.can_make_class(classroom):
                    volunteer.possible_classrooms += 1
                    classroom.possible_volunteers += 1
        self.individuals.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_volunteers)

        

