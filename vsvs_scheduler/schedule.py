import csv
import os
import warnings



class ApplicationScheduler:

    def __init__(self, max_size: int = 4):
        self.max_team_size: int = max_size
        self.classroom_list: list[Classroom] = []
        self.applicant_list: list[Applicant] = []

    def assign_volunteers(self):
        for applicant in self.applicant_list:
            class_idx = 0
            while applicant.group_num == -1 and class_idx < len(self.classroom_list):
                classroom = self.classroom_list[class_idx]
                if classroom.can_make_class(applicant) and classroom.num_of_volunteers < self.max_team_size:
                    classroom.assign(applicant)
                else:
                    class_idx += 1
            if applicant.group_num == -1:
                warnings.warn(f'WARNING:{str(applicant)} could not be assigned to a classroom because of scheduling '
                              f'conflicts.')
            # Sorts the classroom_list from least to greatest number of volunteers assigned.
            self.classroom_list.sort(key=lambda classroom: classroom.num_of_volunteers, reverse=True)


class Schedule:

    def __init__(self, applications: ApplicationScheduler, max_team_size: int = 4, min_team_size: int = 3):
        self.max_team_size = max_team_size
        self.min_team_size = min_team_size

        self.find_class_for_partners()
        self.assign_team_leaders()
        self.assign_volunteers()
        self.assign_second_time()

    def assign_second_time(self):
        """Unassigns all volunteers from a classroom

                :return: list of the volunteers that were unassigned
                """
        self.sort_classrooms_by_num_of_volunteers()
        for classroom in self.classroom_list:
            if classroom.num_of_volunteers < self.min_team_size:
                group_num = classroom.group_number
                for volunteer in self.volunteer_list:
                    if volunteer.group_number == group_num:
                        volunteer.group_number = -1
                        volunteer.assigned_leader = False
                        classroom.number_of_volunteers = 0
                        classroom.team_leader = False
        self.assign_volunteers()

    def find_class_for_partners(self):
        """
        Assigns partners to a classroom they all can make based on parnters.free_time. When classroom is found,
        classroom.assign_partners is used to assign them.

        :return:
        """
        self.sort_classrooms_by_num_of_volunteers()
        for partners in self.partner_groups:
            class_idx = 0
            while partners.group_number == -1 and class_idx < len(self.classroom_list):
                curr_class = self.classroom_list[class_idx]
                if curr_class.can_make_class(partners.availability) & (
                        self.max_team_size - curr_class.num_of_volunteers):
                    curr_class.assign_partners(partners)
                else:
                    class_idx += 1
            if partners.group_number == -1:
                warnings.warn(f'WARNING:{str(partners)} partner group could not be assigned together because of '
                              'scheduling conflicts.')
        self.sort_by_availability()
