from datetime import datetime, timedelta

from vsvs_scheduler.classroom import Classroom


class Volunteer:
    first_time = datetime.strptime("7:15", "%H:%M")
    last_time = datetime.strptime("15:30", "%H:%M")

    def __init__(self, first: str, last: str, phone: str, email: str, leader_app: bool, imported_schedule: list,
                 after_school: list, robotics_interest: bool = False, special_needs_interest: bool = False,
                 board_member: bool = False):
        """

        :param first: first name test
        :param last: last name
        :param phone: cell
        :param email: vandy email test
        :param leader_app:
        :param imported_schedule: array containing an element for each 15-min block for 7:15am-3:45pm. Each element is a
        string of letters that indicate the weekdays in which the volunteer has commitments during the time block.
        :param after_school:
        :param board_member:
        """

        # imported_schedule: array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday
        # (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.)
        # value at an index is 1 if volunteer is available at that time and 0 if they are busy
        #
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email.lower()
        self.board = board_member
        self.leader_app = leader_app or board_member  # if volunteer applied to be a team leader or is board member

        self.after_school = after_school
        self.availability = self.create_availability_schedule(imported_schedule)

        self.group_number = -1  # -1 means unassigned
        self.assigned_leader = False  # Was the volunteer assigned to be their group's team leader?
        self.possible_classrooms = 0  # number of classrooms the volunteer can make

    def create_availability_schedule(self, raw_schedule: list):
        unavailability_schedule = self.convert_to_unavailability_dict(raw_schedule)

        # each day of the week has a dictionary with a key corresponding to the time of day and a value corresponding
        # the minutes of consecutive free time the volunteer has starting at that time
        weekly_availability = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}}

        for day in unavailability_schedule:
            # checks that the unavailability schedule for the day exists/ is nonempty
            if unavailability_schedule[day]:
                weekly_availability[day] = self.find_day_availability(unavailability_schedule[day])

        return weekly_availability

    def find_day_availability(self, day_schedule: list[datetime]):
        day_availability = {}

        # initialize loop vars
        idx = 0
        next_unavailable_time = day_schedule[0]
        current_time = self.first_time

        while current_time < datetime.strptime("17:00", "%H:%M"):
            while next_unavailable_time >= current_time:
                time_available = int((next_unavailable_time - current_time).seconds / 60)  # time in minutes
                if time_available > 0:
                    # adds free time left from current time into current weekday dictionary in weekly_free_time
                    day_availability[current_time] = time_available
                current_time += timedelta(minutes=15)
            if idx == len(day_schedule) - 1:
                next_unavailable_time = datetime.strptime("17:00", "%H:%M")
            else:
                idx += 1
                next_unavailable_time = day_schedule[idx]  # check next unavailable time
        return day_availability

    def convert_to_unavailability_dict(self, raw_schedule: list):
        """Converts the schedule imported from individuals.csv into a schedule_dictionary. This is used by
        create_availability_schedule. {'Monday': [ ], 'Tuesday': [ ], 'Wednesday': [ ], 'Thursday': [ ]}

        :param raw_schedule: each element is a 15-min block & the letters are the weekdays the volunteer is busy
        :return: dict with list of datetime objects of 15-min blocks when the volunteer is busy for each weekday.
        """
        schedule_dict = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}
        week_days = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday'}

        current_time = self.first_time
        idx = 0

        # for each 15-minute time block, check what days volunteer is busy and add the time
        while current_time < self.last_time:
            for day in raw_schedule[idx].split(', '):
                if day == "":  # for times during which the volunteer is not available any day of the week
                    continue
                weekday = week_days[day]
                schedule_dict[weekday].append(current_time)
            current_time = current_time + timedelta(minutes=15)  # increment time by 15 minutes at the end of each loop
            idx += 1  # look at the next element of the raw_schedule for the next loop

        for day in week_days:
            if day not in self.after_school:
                current_time = self.last_time
                weekday = week_days[day]
                while current_time < datetime.strptime("17:00", "%H:%M"):
                    schedule_dict[weekday].append(current_time)
                    current_time = current_time + timedelta(minutes=15)

        return schedule_dict

    def can_make_class(self, classroom: Classroom):
        """Returns boolean of whether volunteer/partner group can make a classroom based on the schedule parameter.

        :param classroom:
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
        time = time - timedelta(minutes=30)

        if time in schedule[classroom.weekday]:
            return schedule[classroom.weekday][time] >= classroom.duration()

        return False


class Partners:
    def __init__(self, group: list[Volunteer]):
        self.members = group
        self.possible_classrooms = 0
        self.group_number = -1

    def can_make_class(self, classroom: Classroom):
        for member in self.members:
            if not member.can_make_class(classroom):
                return False
        return True

    def increment_possible_classrooms(self):
        self.possible_classrooms += 1
        for member in self.members:
            member.possible_classrooms += 1

    def assign_partners(self, classroom: Classroom):
        for member in self.members:
            classroom.assign_volunteer(member)
        self.group_number = classroom.group_number

    def __str__(self):
        result = ""
        for member in self.members:
            result += member.__str__
        return result
