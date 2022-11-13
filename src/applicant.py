from datetime import datetime, timedelta
from src.partners import Partners


class Applicant:
    """Base class that the Volunteer and the Classroom classes inherit from."""

    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

        # Defaults
        self.group_number = -1  # group number of -1 means not assigned to a group
        self.grade_level = 0
        self.robotics = False
        self.special_needs = False
        self.weekday = "Not assigned"
        self.start_time = datetime.today()
        self.end_time = datetime.today()
        self.first_time = "07:15"
        self.last_time = "15:30"

    def set_times(self, start: str, end: str):
        self.start_time = datetime.strptime(start, '%I:%M:%S %p')
        self.end_time = datetime.strptime(end, '%I:%M:%S %p')


class Volunteer(Applicant):

    def __init__(self, name: str, phone: str, email: str, team_leader_app: bool, imported_schedule: list):
        """
        :param name:
        :param phone:
        :param email:
        :param team_leader_app: Did they apply to be a team leader? Yes=true, No=false
        :param index: volunteer index in the volunteer_list
        :param imported_schedule: A list with an element for each 15-min block between the times of 7:15am-3:45pm,
                                  Monday through Thursday. The elements in the list are each a string of letters. The
                                  letters in the string indicate the days of the week during which the volunteer is not
                                  available for that time block.
        """
        super().__init__(name, phone, email)
        self.leader_app = team_leader_app
        self.free_time = self.schedule_to_free_time(imported_schedule)

        self.classrooms_possible = 0  # Number of classrooms the volunteer can make according to their schedule
        self.leader = False  # Was the volunteer assigned to be their group's team leader?

    def __str__(self):
        return self.name

    def schedule_to_free_time(self, schedule: list):
        """

        :param schedule:
        :return:
        """
        unavailability_schedule = self.convert_imported_list_to_schedule_dict(schedule)
        start_time = datetime.strptime(self.first_time, "%H:%M")
        end_time = datetime.strptime(self.last_time, "%H:%M")

        # each day of the week has a dictionary with a key corresponding to the time of day and a value corresponding
        # the minutes of consecutive free time the volunteer has starting at that time
        weekly_free_time = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}}

        for day in unavailability_schedule:
            current_time = start_time
            day_free_time = weekly_free_time[day]  # dictionary that will keep track of free time for that weekday
            if unavailability_schedule[day]:  # checks that the unavailability schedule for the day exists/ is nonempty
                idx = 0
                next_unavailable_time = unavailability_schedule[day][idx]
            else:
                next_unavailable_time = end_time  # if no unavailability schedule for day, person is available all day
            while current_time < end_time:
                while next_unavailable_time >= current_time:
                    time_available = int((next_unavailable_time - current_time).total_seconds() / 60)  # time in minutes
                    if time_available > 0:
                        # adds free time left from current time into current weekday dictionary in weekly_free_time
                        day_free_time[current_time.strftime('%H:%M')] = time_available
                    current_time += timedelta(minutes=15)  # increases current time by 15 minutes
                if next_unavailable_time == end_time:
                    pass  # no need to check next unavailable time in unavailability_schedule
                elif idx == len(unavailability_schedule[day]) - 1 and unavailability_schedule[day][idx] != end_time:
                    next_unavailable_time = end_time  # if no more unavailability, next unavailable time is end of day
                else:
                    idx += 1
                    next_unavailable_time = unavailability_schedule[day][idx]  # check next unavailable time
        return weekly_free_time

    def convert_imported_list_to_schedule_dict(self, raw_schedule: list):
        """Converts the schedule imported from individuals.csv into a schedule_dictionary.

        :param raw_schedule: each element represents a 15-min block & the letters are the weekdays the volunteer is busy
        :return: dictionary with a list of datetime objects that represent 15-minute time blocks of when the volunteer
        is busy for each weekday. {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}
        """
        weekly_schedule = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}
        start_time = datetime.strptime(self.first_time, "%H:%M")
        end_time = datetime.strptime(self.last_time, "%H:%M")

        current_time = start_time
        idx = 0

        # for each 15-minute time block, check if volunteer is busy
        while current_time < end_time:
            if 'M' in raw_schedule[idx]:
                weekly_schedule['Monday'].append(current_time)
            if 'T' in raw_schedule[idx]:
                weekly_schedule['Tuesday'].append(current_time)
            if 'W' in raw_schedule[idx]:
                weekly_schedule['Wednesday'].append(current_time)
            if 'R' in raw_schedule[idx]:
                weekly_schedule['Thursday'].append(current_time)
            current_time = current_time + timedelta(minutes=15)  # increment time by 15 minutes at the end of each loop
            idx += 1  # look at the next element of the raw_schedule for the next loop

        return weekly_schedule


class Classroom(Applicant):

    def __init__(self, name: str, phone: str, email: str, group_number: int, school: str, start_time: str,
                 end_time: str):
        super().__init__(name, phone, email)
        self.group_number = group_number
        self.weekday = "Monday"
        self.set_times(start_time, end_time)
        self.num_of_volunteers = 0
        self.school = school
        self.team_leader = False  # has a team leader?

    def free_time_duration(self):
        """:returns: minutes of free time needed to perform a lesson, including driving and teaching time."""
        return (self.end_time - self.start_time + timedelta(minutes=30)).total_seconds() / 60

    def can_make_class(self, schedule: dict):
        """Returns boolean of whether volunteer/partner group can make a classroom based on the schedule parameter.

        :param schedule: free time schedule of a volunteer or partner group
        :return: bool: whether volunteer/partners can make that class
        """
        time_deviation = self.start_time.minute % 15
        if time_deviation != 0:
            new_time = self.start_time - timedelta(minutes=time_deviation)
            time = new_time.strftime('%H:%M')
        else:
            time = self.start_time.strftime('%H:%M')

        if time in schedule[self.weekday]:
            return schedule[self.weekday][time] >= self.free_time_duration()
        else:
            return False

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
        return self.name + ' at ' + self.school
