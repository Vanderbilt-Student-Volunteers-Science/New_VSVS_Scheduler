import re


def convert_to_free_time_array(schedule_array):
    """ Converts the array of times in week order (output of convert_to_schedule_array) to an array where value at each
    time index corresponds to how much free time they have starting at that index. For example, if I am free from 10:00
    to 11:30 on Monday, index 11 (10:00-10:15) will become 90, index 12 (10:15-10:30) will become 75, index 17
    (11:30-11:45) will become 0, etc.

    :param schedule_array:array containing an index for each 15-min block between the times of 7:15am-3:45pm,
    Monday through Thursday (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101 are
    Wednesday, etc.); value at an index is 1 if volunteer is available at that time and 0 if they are busy

    :return: free_time_array: array where indices are the same as schedule_array but the value at each index is the
    minutes of consecutive free time the volunteer has starting at that time
    """
    free_time_array = []

    # i is the index being set, j is the index being tested for availability
    for i in range(136):
        j = i
        consecutive_free_time = 0
        while j < 136 and schedule_array[j] == 1 and (
                j % 34 != 0 or j == i):  # (j % 34 != 0 or j == i) prevents overlap into new day
            j += 1
            consecutive_free_time += 15
        free_time_array.append(consecutive_free_time)

    return free_time_array


def calculate_free_time_start(class_start_time, school_travel_time):
    """ Returns the first time a volunteer needs to be free to perform a lesson in military time.

    :param class_start_time: time class starts in military time
    :param school_travel_time: time it takes to travel to school one-way in minutes
    :return:
    """
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

# TODO: import travel times directly from globalAttributes to here
# TODO: use ints not floats
