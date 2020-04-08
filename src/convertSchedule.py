# Used in volunteer.py, partners.py, and classroom.py


def convert_to_military(time):
    time_list = time.split(':', 2)  # split into hours, minutes AM/PM
    time_list2 = time_list[1].split(' ', 2)  # split into minutes, AM/PM

    if time_list2[1] == 'AM' or time_list[0] == '12':
        return (100 * int(time_list[0])) + int(time_list2[0])
    else:
        return 1200 + (100 * int(time_list[0])) + int(time_list2[0])


# Converts the schedule imported from individuals.csv, columns of times containing days volunteers can't make that time,
# into array of times in week order (each index is a 15-min increment - indexes 0-33 are Monday 7:15am to 3:45pm,
# 34-67 are Tuesday 7:15-3:45, 68-101 are Wednesday, etc.) listing a 1 if a volunteer is available and a 0 if they aren't
def convert_to_schedule_array(imported_schedule):
    output_array = [1] * 136
    for i in range(34):
        if 'M' in imported_schedule[i]:
            output_array[i] = 0
        if 'T' in imported_schedule[i]:
            output_array[34 + i] = 0
        if 'W' in imported_schedule[i]:
            output_array[68 + i] = 0
        if 'H' in imported_schedule[i]:
            output_array[102 + i] = 0
    return output_array


# - Converts the array of times in week order (output of convert_to_schedule_array) to an array where value at each time index corresponds to how much free
# time they have starting at that index. For example, if I am free from 10:00 to 11:30 on Monday, index 11 (10:00-10:15) will
# become 90, index 12 (10:15-10:30) will become 75, index 17 (11:30-11:45) will become 0, etc.
# - input: 34 entries per day (for 4 weekdays) starting at 7:15am, each index represents 15 min increments; 1 is
# available, 0 is unavailable
# - output: array where value at each time is minutes of consecutive free time they have starting at that time
def convert_schedule_array(schedule_array):
    output_array = []

    # i is the index being set, j is the index being tested for availability
    for i in range(136):
        j = i
        consecutive_free_time = 0
        while j < 136 and schedule_array[j] == 1 and (j % 34 != 0 or j == i): #  (j % 34 != 0 or j == i) prevents overlap into new day
            j += 1
            consecutive_free_time += 15
        output_array.append(consecutive_free_time)

    return output_array


#  returns first time volunteer needs to be free to perform a lesson in military time
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
    else:  # day_of_week == "Thursday":
        day = 3
    hour = int(free_time_start / 100)
    min = free_time_start % 100
    min = int(min / 15) * 15
    if min == 0:
        return int((34 * day) + ((hour - 8) * 4) + 3)
    return int((34 * day) + ((hour - 7) * 4) + ((min - 15) / 15))
