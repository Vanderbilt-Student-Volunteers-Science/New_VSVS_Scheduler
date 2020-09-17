import src.globalAttributes
import re

# Converts input time to military time.
# time - time with AM or PM; ex: "2:05 PM"
def convert_to_military(time):
    # use regular expressions to split string into three groups for hour, min, AM/PM
    # groups in the regex are set off with parentheses
    # [\d]* means one or more numbers
    # [A|P]M means AM or PM
    regex = r'([\d]*):([\d]*) ([A|P]M)'
    try:
        # search the time string for this regex pattern
        # then, select groups 1, 2, and 3 and save them as hour, min, am_pm
        hour, minute, am_pm = re.search(regex, time).group(1,2,3)
    except:
        raise ValueError('{} is an invalid time string.'.format(time))

    if am_pm == 'AM' or hour == '12':
        return (100 * int(hour)) + int(minute)
    else:
        return 1200 + (100 * int(hour)) + int(minute)


# Converts the schedule imported from individuals.csv into a schedule_array.
# imported_schedule - array of days of the week a volunteer is busy; each index corresponds to a time of day and the
#                     letters at the index indicate the days of the week the volunteer is busy at that time
# schedule_array -    array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday
#                     through Thursday (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101
#                     are Wednesday, etc.); value at an index is 1 if volunteer is available at that time and 0 if they
#                     are busy
def convert_to_schedule_array(imported_schedule):
    schedule_array = [1] * 136
    for i in range(34):
        if 'M' in imported_schedule[i]:
            schedule_array[i] = 0
        if 'T' in imported_schedule[i]:
            schedule_array[34 + i] = 0
        if 'W' in imported_schedule[i]:
            schedule_array[68 + i] = 0
        if 'R' in imported_schedule[i]:
            schedule_array[102 + i] = 0
    return schedule_array


# Converts the array of times in week order (output of convert_to_schedule_array) to an array where value at each time
# index corresponds to how much free time they have starting at that index. For example, if I am free from 10:00 to
# 11:30 on Monday, index 11 (10:00-10:15) will become 90, index 12 (10:15-10:30) will become 75, index 17 (11:30-11:45)
# will become 0, etc.
# schedule_array -  array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday
#                   through Thursday (indexes 0-33 are Monday 7:15am to 3:45pm, 34-67 are Tuesday 7:15-3:45, 68-101
#                   are Wednesday, etc.); value at an index is 1 if volunteer is available at that time and 0 if they
#                   are busy
# free_time_array - array where indices are the same as schedule_array but the value at each index is the minutes of
#                   consecutive free time the volunteer has starting at that time
def convert_to_free_time_array(schedule_array):
    free_time_array = []

    # i is the index being set, j is the index being tested for availability
    for i in range(136):
        j = i
        consecutive_free_time = 0
        while j < 136 and schedule_array[j] == 1 and (j % 34 != 0 or j == i): # (j % 34 != 0 or j == i) prevents overlap into new day
            j += 1
            consecutive_free_time += 15
        free_time_array.append(consecutive_free_time)

    return free_time_array


# Returns the first time a volunteer needs to be free to perform a lesson in military time.
# class_start_time -   time class starts in military time
# school_travel_time - time it takes to travel to school one-way in minutes
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


# Returns minutes of free time needed to perform a lesson, including driving and teaching time.
# class_start_time -   time class starts in military time
# class_end_time -     time class ends in military time
# school_travel_time - time it takes to travel to school one-way in minutes
# TODO: import travel times directly from globalAttributes to here
# TODO: use ints not floats
def calculate_free_time_needed(class_start_time, class_end_time, school_travel_time):
    class_start_minutes = class_start_time % 100
    class_start_hours = (class_start_time - class_start_minutes) / 100  # 1PM is 13 (NOT 1300)
    class_end_minutes = class_end_time % 100
    class_end_hours = (class_end_time - class_end_minutes) / 100
    if class_start_hours == class_end_hours:
        # TODO: change from (1 * school_travel_time) to (2 * school_travel_time) to account for driving time both ways
        return int(class_end_minutes - class_start_minutes + (1 * school_travel_time))
    else:  # start_hour < end_hour
        # TODO: change from (1 * school_travel_time) to (2 * school_travel_time) to account for driving time both ways
        # changed because we only need 15 mins at beginning of lesson for teams to review their lessons (no travel time this semester)
        return int((60 - class_start_minutes) + (60 * (class_end_hours - class_start_hours - 1)) + class_end_minutes + (1 * school_travel_time))


# Returns the index in a free_time_array that corresponds to the time (and day of week) a lesson starts.
# day_of_week -     day of the week the lesson takes place
# free_time_start - the first time a volunteer needs to be free to perform a lesson in military time
def military_to_free_time_array(day_of_week, free_time_start):
    if day_of_week == "Monday":
        day = 0
    elif day_of_week == "Tuesday":
        day = 1
    elif day_of_week == "Wednesday":
        day = 2
    elif day_of_week == "Thursday":
        day = 3
    else:
        raise ValueError('{} is an invalid day of the week.'.format(day_of_week))

    hour = int(free_time_start / 100)
    min = free_time_start % 100
    min = int(min / 15) * 15
    if min == 0:
        return int((34 * day) + ((hour - 8) * 4) + 3)
    return int((34 * day) + ((hour - 7) * 4) + ((min - 15) / 15))


# Creates a free_time_array for a group of partners.
# volunteer_schedule_array - schedule_array of the Volunteer object for the first partner in the group; the Volunteer
#                            object where the partner_free_time_array will be stored
# num_partners -             number of people in the group - 1 (number of people other than the first partner in the
#                            group)
# partner_indexes -          indexes of the Volunteer objects in volunteer_list corresponding to all of them members in
#                            the group (except the first partner)
def create_partner_schedule(volunteer_schedule_array, num_partners, partner_indexes):
    partner_schedule_array = []

    if num_partners == 1:
        partner_schedule_array = schedule_array_and(volunteer_schedule_array, src.globalAttributes.volunteer_list[partner_indexes[0]].schedule_array)
    elif num_partners == 2:
        partner_schedule_array = schedule_array_and(schedule_array_and(volunteer_schedule_array, src.globalAttributes.volunteer_list[partner_indexes[0]].schedule_array), src.globalAttributes.volunteer_list[partner_indexes[1]].schedule_array)
    else:
        partner_schedule_array = schedule_array_and(schedule_array_and(volunteer_schedule_array, src.globalAttributes.volunteer_list[partner_indexes[0]].schedule_array), schedule_array_and(src.globalAttributes.volunteer_list[partner_indexes[1]].schedule_array, src.globalAttributes.volunteer_list[partner_indexes[2]].schedule_array))

    return convert_to_free_time_array(partner_schedule_array)


# Helper function for create_partner_schedule. Computes the 'and' schedule array of two schedule arrays.
def schedule_array_and(schedule_array1, schedule_array2):
    output_array = []
    for schedule_index in range(len(schedule_array1)):
        output_array.append(schedule_array1[schedule_index] and schedule_array2[schedule_index])

    return output_array

