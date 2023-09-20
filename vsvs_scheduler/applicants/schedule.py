
from datetime import timedelta, datetime
from .classroom import Classroom


class Schedule:
    def __init__(self, raw_schedule: list) -> None:
        """ Initializes the schedule object """

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
        """ Processes the raw schedule into a dictionary of the form {day: {time: duration}} """

        availability = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': []}
        current_time = self.first_time
        idx = 0


        while current_time < self.last_time:
            for day in raw_schedule[idx].split(', '): 
                if day == "": 
                    continue
                availability[day].append(current_time)
            
            current_time += timedelta(minutes=15)  # look at the next 15 minute time block
            idx += 1  

        self.find_free_time_duration(availability)



    def find_free_time_duration(self, availability: dict):
        """ Finds the duration of free time for each time block in the schedule """

        for day, day_availability in availability.items(): 

            # if the volunteer is not available on that day, skip the day
            if day_availability == []: 
                continue

            # schedule for the day
            day_schedule = self.processed_schedule[day]

            idx = 0 # index of the current time block
            current_time = day_availability[idx] # current time block
            time_available = 0
           

            # while there are still time blocks to look at
            while (idx + 2) <= len(day_availability) :
                # time block being tracked for availability
                time_being_tracked_for_availability = day_availability[idx]

                # if the next time block is 15 minutes after the current time block, add 15 minutes to the time available
                while (idx + 2) <= len(day_availability) and day_availability[idx + 1] == current_time + timedelta(minutes=15):
                    time_available += 15 
                    idx += 1
                    current_time += timedelta(minutes=15)
                    
                # if the next time block is not 15 minutes after the current time block, add the time available to the schedule
                time_available += 15
                day_schedule[time_being_tracked_for_availability] = time_available
                time_available = 0 
                idx += 1
                current_time += timedelta(minutes=15)


                
    def can_make_class(self, classroom: Classroom, last_round: bool = False) -> bool:
        """ Returns True if the volunteer can make the class, False otherwise."""
        if last_round and classroom.weekday != None:
            weekday = classroom.weekday
        else:
            weekday = classroom.teacher.weekday
        
        # Standardize the start time to the nearest 15 minute interval
        time_deviation = classroom.start_time.minute % 15
        if time_deviation != 0:
            start_time = classroom.start_time - timedelta(minutes=time_deviation)
        else:
            start_time = classroom.start_time

        # Volunteer schedule for the day of the class
        weekday_schedule = self.processed_schedule[weekday]

        if start_time in weekday_schedule:
            return weekday_schedule[start_time] >= classroom.duration()
        
        available_times = list(weekday_schedule.keys())

        # check if there is a time block that begins before the start time 
        if len(weekday_schedule) >= 1 and available_times[0] < start_time:
            idx = 0
            while idx < len(weekday_schedule) and available_times[idx] < start_time:
                curr_time = available_times[idx]
                # time required to make the class
                time_required = ((start_time - curr_time).seconds/60) + classroom.duration()
                if weekday_schedule[curr_time] >= time_required:
                    return True
                idx += 1

        return False



