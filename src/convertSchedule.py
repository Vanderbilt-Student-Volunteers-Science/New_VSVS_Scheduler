# Used in volunteer.py, partners.py, and classroom.py


class ConvertSchedule:

    def convert_to_military(time):
        time_list = time.split(':', 2)  # split into hours, minutes AM/PM
        time_list2 = time_list[1].split(' ', 2)  # split into minutes, AM/PM

        if time_list2[1] == 'AM':
            return (100 * time_list[0]) + time_list2[0]
        else:
            return 1200 + (100 * time_list[0]) + time_list2[0]

    # - Converts the Volunteer schedule array into array where value at each time index corresponds to how much free
    # time they have starting at that index. For example, if I am free from 10:00 to 11:30, index 12 (10:00) will
    # become 90, index 13 (10:15) will become 75, index 18 (11:30) will become 0, etc.
    # - input: 40 entries per day (for 5 weekdays) starting at 7:00 AM, each index represents 15 min increments; 2 is
    # busy, 1 is available, 0 is blank
    # - output: array where value at each time is minutes of consecutive free time they have starting at that time
    def convert_schedule_array(schedule_array):
        output_array = []
        for i in range(200):
            j = i
            consecutive_free_time = 0
            while (schedule_array[j] == 1) and ((j - 1) % 40 != 1) and (j < 200): #  ((j - 1) % 40 == 1) means first block of a new day
                j += 1
                consecutive_free_time += 15
            output_array[i] = consecutive_free_time

    #  returns first time volunteer needs to be free to perform a lesson
    def calculate_free_time_start(class_start_time, school_travel_time):
        class_start_minutes = class_start_time % 100
        if class_start_minutes >= school_travel_time:
            return class_start_time - school_travel_time
        else:
            class_start_hours = class_start_time - class_start_minutes
            hours_away = int((school_travel_time - class_start_minutes) / 60)
            minutes_away = (school_travel_time - class_start_minutes) % 60
            if minutes_away == 0:
                return class_start_hours - (hours_away * 100)
            else:
                return class_start_hours - ((hours_away + 1) * 100) + (60 - minutes_away)

    #  returns minutes of free time needed to perform a lesson, taking into account school distance
    def calculate_free_time_needed(class_start_time, class_end_time, school_travel_time):
        class_start_minutes = class_start_time % 100
        class_start_hours = (class_start_time - class_start_minutes) / 100  # 1PM is 13 (NOT 1300)
        class_end_minutes = class_end_time % 100
        class_end_hours = (class_end_time - class_end_minutes) / 100
        if class_start_hours == class_end_hours:
            return class_end_minutes - class_start_minutes + (2 * school_travel_time)
        else:  # start_hour < end_hour
            return (60 - class_start_minutes) + (60 * (class_end_hours - class_start_hours - 1)) + class_end_minutes + (2 * school_travel_time)

    def military_to_schedule_array(day_of_week, free_time_start):
        if day_of_week == "Monday":
            day = 0
        elif day_of_week == "Tuesday":
            day = 1
        elif day_of_week == "Wednesday":
            day = 2
        elif day_of_week == "Thursday":
            day = 3
        else:  # day_of_week == "Friday":
            day = 4
        hour = int(free_time_start / 100)
        min = free_time_start % 100
        return (40 * day) + (4 * (hour - 7)) + int(min / 15)


#  don't depend on ConvertSchedule objects (there are none)
ConvertSchedule.convert_to_military = staticmethod(ConvertSchedule.convert_to_military)
ConvertSchedule.convert_schedule_array = staticmethod(ConvertSchedule.convert_schedule_array)
ConvertSchedule.calculate_free_time_start = staticmethod(ConvertSchedule.calculate_free_time_start)
ConvertSchedule.calculate_free_time_needed = staticmethod(ConvertSchedule.calculate_free_time_needed)
ConvertSchedule.military_to_schedule_array = staticmethod(ConvertSchedule.military_to_schedule_array)
