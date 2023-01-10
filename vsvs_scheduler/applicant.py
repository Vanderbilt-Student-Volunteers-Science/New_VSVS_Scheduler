from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Applicant(ABC):
    """Base class that the Volunteer and the Partners classes inherit from."""
    first_time = datetime.strptime("7:15", "%H:%M")
    last_time = datetime.strptime("15:30", "%H:%M")

    def __init__(self, team_leader: bool = False):
        """

        :param team_leader: interest in being team leader
        """
        self.email = None
        self.group_num: int = -1
        self.availability = self.create_availability_schedule()
        self.robotics: bool = False
        self.special_needs: bool = False
        self.leader_app: bool = team_leader
        self.classrooms_possible: int = 0  # Number of classrooms the volunteer can make according to their schedule
        super(Applicant, self).__init__()

    @abstractmethod
    def create_availability_schedule(self):
        pass

    @abstractmethod
    def assign(self):
        pass

    def __str__(self):
        text_output = ""
        volunteers = self.assign()
        if volunteers is list:
            for volunteer in volunteers:
                if volunteer == volunteers[-1]:
                    text_output += str(volunteer)
                else:
                    text_output += str(volunteer) + ", "
        else:
            text_output += volunteers.name
        return text_output


class Volunteer(Applicant):
    def __init__(self, name: str, phone: str, email: str, team_leader_app: bool, imported_schedule: list):
        """
        :param team_leader_app: interest in being team leader
        :param imported_schedule: A list with an element for each 15-min block between the times of 7:15am-3:45pm,
                                  Monday through Thursday. The elements in the list are each a string of letters. The
                                  letters in the string indicate the days of the week during which the volunteer is not
                                  available for that time block.
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.raw_schedule = imported_schedule
        super().__init__(team_leader_app)

    def create_availability_schedule(self):
        unavailability_schedule = self.convert_raw_schedule_to_dict(self.raw_schedule)

        # each day of the week has a dictionary with a key corresponding to the time of day and a value corresponding
        # the minutes of consecutive free time the volunteer has starting at that time
        weekly_availability = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}}

        for day in unavailability_schedule:
            # checks that the unavailability schedule for the day exists/ is nonempty
            if unavailability_schedule[day]:
                weekly_availability[day] = self.day_availability(unavailability_schedule[day])

        return weekly_availability

    def day_availability(self, day_schedule: list[datetime]):
        day_availability = {}

        # initialize loop vars
        idx = 0
        next_unavailable_time = day_schedule[0]
        current_time = self.first_time

        while current_time < self.last_time:
            while next_unavailable_time >= current_time:
                time_available = int((next_unavailable_time - current_time).total_seconds() / 60)  # time in minutes
                if time_available > 0:
                    # adds free time left from current time into current weekday dictionary in weekly_free_time
                    day_availability[current_time.time] = time_available
                current_time += timedelta(minutes=15)
            if idx == len(day_schedule) - 1:
                next_unavailable_time = self.last_time
            else:
                idx += 1
                next_unavailable_time = day_schedule[idx]  # check next unavailable time
        return day_availability

    def convert_raw_schedule_to_dict(self, raw_schedule: list[str]):
        """Converts the schedule imported from individuals.csv into a schedule_dictionary. This is used by
        create_availability_schedule. {'Monday': [ ], 'Tuesday': [ ], 'Wednesday': [ ], 'Thursday': [ ]}

        :param raw_schedule: each element is a 15-min block & the letters are the weekdays the volunteer is busy
        :return: dict with list of datetime objects of 15-min blocks when the volunteer is busy for each weekday.
        """
        schedule_dict = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}

        current_time = self.first_time
        idx = 0

        # for each 15-minute time block, check what days volunteer is busy and add the time
        while current_time < self.last_time:
            if 'M' in raw_schedule[idx]:
                schedule_dict['Monday'].append(current_time)
            if 'T' in raw_schedule[idx]:
                schedule_dict['Tuesday'].append(current_time)
            if 'W' in raw_schedule[idx]:
                schedule_dict['Wednesday'].append(current_time)
            if 'R' in raw_schedule[idx]:
                schedule_dict['Thursday'].append(current_time)
            current_time = current_time + timedelta(minutes=15)  # increment time by 15 minutes at the end of each loop
            idx += 1  # look at the next element of the raw_schedule for the next loop

        return schedule_dict

    def assign(self):
        return self

    def __repr__(self):
        return self.name


class Partners(Applicant):
    def __init__(self, volunteers_list: list):
        """

        :param volunteers_list:
        """
        self.volunteers: list[Volunteer] = volunteers_list
        self.group_size = len(volunteers_list)
        super().__init__()

    def create_availability_schedule(self):
        """

        :return:
        """
        partners_schedule = {}

        # for all volunteers in group
        for idx in range(len(self.volunteers)):
            curr_volunteer = self.volunteers[idx].availability
            if idx == 0:
                # If it's the first partner (idx = 0), then just copy their schedule into partners_schedule
                partners_schedule = curr_volunteer
            else:
                for day in partners_schedule:
                    for time in partners_schedule[day].copy():
                        # If not the first partner and the time is not in partners_schedule then just skip
                        if time not in curr_volunteer[day]:
                            del partners_schedule[day][time]
                        # If not the first partner and the time in partners_schedule, check if partners_schedule or
                        # curr_volunteer has less free time at the time. Keep the one with the least time.
                        elif curr_volunteer[day][time] < partners_schedule[day][time]:
                            partners_schedule[day][time] = curr_volunteer[day][time]
        return partners_schedule

    def assign(self):
        return self.volunteers
