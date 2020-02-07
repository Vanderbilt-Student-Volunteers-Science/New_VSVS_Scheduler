# Used in volunteer.py, partners.py, and classroom.py

class ConvertSchedule:

    # input: 40 entries per day (for 5 weekdays), each index represents 15 min increments; 2 is busy, 1 is available, 0 is blank
    # output: array where value at each time is minutes of consecutive free time they have starting at that time
    def convert_schedule_array(schedule_array):
        output_array = []
        for i in range(200):
            j = i
            consecutive_free_time = 0
            while (schedule_array[j] == 1) and ((j - 1) % 40 != 1) and (j < 200): #  ((j - 1) % 40 == 1) means first block of a new day
                j += 1
                consecutive_free_time += 15
            output_array[i] = consecutive_free_time

    def convert_to_military(time):
        time_list = time.split(':', 2)
        time_list2 = time_list[1].split(' ', 2)  # split into minutes and AM/PM

        if time_list2[1] == 'AM':
            return (100 * time_list[0]) + time_list2[0]
        else:
            return 1200 + (100 * time_list[0]) + time_list2[0]


#  don't depend on ConvertSchedule objects (there are none)
ConvertSchedule.convert_schedule_array = staticmethod(ConvertSchedule.convert_schedule_array)
ConvertSchedule.convert_to_military = staticmethod(ConvertSchedule.convert_to_military)
