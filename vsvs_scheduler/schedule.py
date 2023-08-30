
from datetime import timedelta, datetime
from classroom import Classroom


class Schedule:

    def __init__(self, raw_schedule: list) -> None:

        self.first_time = datetime.strptime("7:15", "%H:%M")
        self.last_time = datetime.strptime("17:15", "%H:%M")

        # schedule for each day of the week
        self.Monday = {}
        self.Tuesday = {}
        self.Wednesday = {}
        self.Thursday = {}

        self.processed_schedule = {'Monday': self.Monday, 
                                   'Tuesday': self.Tuesday, 
                                   'Wednesday': self.Wednesday, 
                                   'Thursday': self.Thursday}

        self.process_raw_schedule(raw_schedule)

    
    def process_raw_schedule(self, raw_schedule: list) -> dict:
        """ Processes the raw schedule and adds the times to the availability dictionary """
        availability = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}
        current_time = self.first_time
        idx = 0


        # for each 15-minute time block, check what days volunteer is free and add the time
        while current_time < self.last_time:
            for day in raw_schedule[idx].split(', '): 
                if day == "":  # if there are no letters then they are available every day of the week
                    continue
                availability[day].append(current_time)
            
            current_time += timedelta(minutes=15)  # increment time by 15 minutes at the end of each loop
            idx += 1  # look at the next element of the raw_schedule for the next loop

        self.find_free_time_duration(availability)
    
    def find_free_time_duration(self, availability: dict):
        """ Finds the duration of free time for each time block in the schedule """
        for day, day_availability in availability.items(): # for each day of the week
            if day_availability == []: # if the volunteer is not available on that day
                continue
            day_schedule = self.processed_schedule[day] # get the schedule for that day

            idx = 0 # index of the current time block
            current_time = day_availability[idx] # current time block
            time_available = 0
           

            # for each time block, check if the next time block is 15 minutes after the current time block
            while (idx + 2) <= len(day_availability) :
                time_being_tracked_for_availability = day_availability[idx]
                # if the next time block is 15 minutes after the current time block, add 15 minutes to the time available
                while (idx + 2) <= len(day_availability) and day_availability[idx + 1] == current_time + timedelta(minutes=15):
                    time_available += 15 
                    idx += 1
                    current_time += timedelta(minutes=15)
                    
                # if the next time block is not 15 minutes after the current time block, add the time available to the schedule
                    
                day_schedule[time_being_tracked_for_availability] = time_available
                time_available = 0 
                idx += 1
                current_time += timedelta(minutes=15)
    
    
    def can_make_class(self, classroom: Classroom):
        time_deviation = classroom.start_time.minute % 15
        if time_deviation != 0:
            start_time = classroom.start_time - timedelta(minutes=time_deviation)
        else:
            start_time = classroom.start_time

        weekday_schedule = self.processed_schedule[classroom.weekday]

        if start_time in weekday_schedule:
            return weekday_schedule[start_time] >= classroom.duration()
        else:
            available_times = list(weekday_schedule.keys())
            if len(weekday_schedule) >= 1 and available_times[0] < start_time:
                idx = 0
                while idx < len(weekday_schedule) and available_times[idx] < start_time:
                    curr_time = available_times[idx]
                    time_required = ((start_time - curr_time).seconds/60) + classroom.duration()
                    if weekday_schedule[curr_time] >= time_required:
                        return True
                    idx += 1

        return False



