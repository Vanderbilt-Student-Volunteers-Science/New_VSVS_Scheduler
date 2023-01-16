
from datetime import datetime, timedelta

from vsvs_scheduler.classroom import Classroom


class Volunteer:
    """This class stores volunteer information: name, phone, email, robotics interest, special needs
    interest, leadership application, schedule """
    first_time = datetime.strptime("7:15", "%H:%M")
    last_time = datetime.strptime("15:30", "%H:%M")

    def __init__(self, name: str, phone: str, email: str, leader_app: bool, imported_schedule: list,
                 robotics_interest: bool = False, special_needs_interest: bool = False):
        """
        :param robotics_interest: Are they interested in robotics? Yes=true, No=false
        :param special_needs_interest: Are they interested in working with special needs students? Yes=true, No=false
        :param leader_app: Did they apply to be a team leader? Yes=true, No=false
        :param imported_schedule: array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is 1 if volunteer is available at that time and 0 if they are busy

        A list with an element for each 15-min block. The elements in the list are each a
                                  string of letters. The letters in the string indicate the days of the week during
                                  which the volunteer is not available for that time block.
        """
        self.name = name
        self.phone = phone
        self.email = email.lower()
        self.robotics_interest = robotics_interest
        self.special_needs_interest = special_needs_interest
        self.leader_app = leader_app  # if volunteer applied to be a team leader

        # array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is the minutes of consecutive free time the volunteer has starting at that time
        self.availability = self.create_availability_schedule(imported_schedule)

        # group number of -1 means not assigned to a group
        self.group_number = -1

        # Was the volunteer assigned to be their group's team leader?
        self.assigned_leader = False

        # Number of classrooms the volunteer can make according to their schedule.
        # Set after partners and drivers are assigned.
        self.possible_classrooms = 0

    def create_availability_schedule(self, raw_schedule: list):
        unavailability_schedule = self.convert_raw_schedule_to_dict(raw_schedule)

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
                time_available = int((next_unavailable_time - current_time).seconds / 60)  # time in minutes
                if time_available > 0:
                    # adds free time left from current time into current weekday dictionary in weekly_free_time
                    day_availability[current_time] = time_available
                current_time += timedelta(minutes=15)
            if idx == len(day_schedule) - 1:
                next_unavailable_time = self.last_time
            else:
                idx += 1
                next_unavailable_time = day_schedule[idx]  # check next unavailable time
        return day_availability

    def convert_raw_schedule_to_dict(self, raw_schedule: list):
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

    def can_make_class(self, classroom: Classroom):
        """Returns boolean of whether volunteer/partner group can make a classroom based on the schedule parameter.

        :param volunteers:
        :return: bool: whether volunteer/partners can make that class
        """
        schedule = self.availability
        time_deviation = classroom.start_time.minute % 15
        if time_deviation != 0:
            new_time = classroom.start_time - timedelta(minutes=time_deviation)
            time = new_time
        else:
            time = classroom.start_time

        if time in schedule[classroom.weekday]:
            return schedule[classroom.weekday][time] >= classroom.free_time_duration()

        return False

    def __str__(self):
        return self.name


class Partners:
    def __init__(self, group: list[Volunteer]):
        self.members = group
        self.availability = self.create_availability_schedule()
        self.possible_classrooms = 0
        self.group_number = -1

    def create_availability_schedule(self):
        """

        :return:
        """
        partners_schedule = {}

        # for all volunteers in group
        for curr_partner in self.members:
            if self.members.index(curr_partner) == 0:
                partners_schedule = curr_partner.availability
            else:
                for day in partners_schedule:
                    for time in partners_schedule[day].copy():
                        # If time is not in partners_schedule then just skip
                        if time not in curr_partner.availability[day]:
                            del partners_schedule[day][time]
                        # If not the first partner and the time in partners_schedule, check if partners_schedule or
                        # curr_partner has less free time at the time. Keep the one with the least time.
                        elif curr_partner.availability[day][time] < partners_schedule[day][time]:
                            partners_schedule[day][time] = curr_partner[day][time]
        return partners_schedule

    def can_make_class(self, classroom: Classroom):
        schedule = self.availability
        time_deviation = classroom.start_time.minute % 15
        if time_deviation != 0:
            new_time = classroom.start_time - timedelta(minutes=time_deviation)
            time = new_time
        else:
            time = classroom.start_time

        if time in schedule[classroom.weekday]:
            return schedule[classroom.weekday][time] >= classroom.free_time_duration()

        return False

    def increment_possible_classrooms(self):
        self.possible_classrooms += 1
        for member in self.members:
            member.possible_classrooms += 1

    def assign_partners(self, classroom: Classroom):
        for member in self.members:
            classroom.assign_volunteer(member)
        self.group_number = classroom.group_number
