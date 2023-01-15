from datetime import datetime, timedelta
from vsvs_scheduler.applicant import Applicant, Volunteer, Partners


class Classroom:

    def __init__(self, name: str, phone: str, email: str, group_number: int, school: str, start: str,
                 end: str):
        self.teacher = name
        self.phone = phone
        self.email = email
        self.school = school
        self.weekday = "Monday"
        self.start_time = datetime.strptime(start, '%H:%M')
        self.end_time = datetime.strptime(end, '%H:%M')

        self.team_leader = None
        self.group_number = group_number
        self.volunteers: list[Volunteer] = []
        self.num_of_volunteers = len(self.volunteers)
        self.volunteers_possible = 0



    def free_time_duration(self):
        """:returns: minutes of free time needed to perform a lesson, including driving and teaching time."""
        return (self.end_time - self.start_time + timedelta(minutes=30)).total_seconds() / 60

    def can_make_class(self, volunteers: Applicant):
        """Returns boolean of whether volunteer/partner group can make a classroom based on the schedule parameter.

        :param volunteers:
        :return: bool: whether volunteer/partners can make that class
        """
        schedule = volunteers.availability
        time_deviation = self.start_time.minute % 15
        if time_deviation != 0:
            new_time = self.start_time - timedelta(minutes=time_deviation)
            time = new_time.time
        else:
            time = self.start_time.time

        if time in schedule[self.weekday]:
            volunteers.classrooms_possible += 1
            self.volunteers_possible += 1
            return schedule[self.weekday][time] >= self.free_time_duration()

        return False

    def assign(self, applicant: Applicant):
        applicant.group_num = self.group_number
        volunteers = applicant.assign()
        if volunteers == list:
            for person in volunteers:
                self.volunteers.append(person)
        else:
            self.volunteers.append(volunteers)

        volunteer_idx = 0
        while not self.team_leader and volunteer_idx < self.num_of_volunteers:
            if self.volunteers[volunteer_idx].leader_app:
                self.team_leader = self.volunteers[volunteer_idx]



    def assign_volunteer(self, volunteer: Volunteer):
        """Assigns a volunteer to a classroom.

        Updates the volunteer.group_number with the group number of the classroom. If the classroom doesn't have a team
        leader and the volunteer applied to be one, it sets the Classroom t_leader equal to this volunteer and updates
        volunteer.assigned_t_leader.

        :param volunteer:volunteer being assigned
        """
        self.num_of_volunteers += 1
        volunteer.group_number = self.group_number
        if not self.team_leader and volunteer.leader_app:
            self.team_leader = True
            volunteer.leader = True

    def assign_partners(self, partners: Partners):
        """Updates the group_number for Partners object and assigns each Volunteer object in Partners to this classroom.

        :param partners: Partners object being assigned to this classroom

        """
        partners.group_number = self.group_number
        for volunteer in partners.volunteers:
            self.assign_volunteer(volunteer)

    def __str__(self):
        return self.teacher + ' at ' + self.school




