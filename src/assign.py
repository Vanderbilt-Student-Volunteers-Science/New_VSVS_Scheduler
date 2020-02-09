import src.volunteer
import src.classroom


# TODO: deal with t_leaders and drivers (only want to assign one)

class Assign:

    def findClassroom(volunteer, classroom_list):
        for group_number in range(1, len(classroom_list)):
            #  if classroom not full, etc.
            if volunteer.schedule[classroom_list[group_number].start_time_schedule_index] >= classroom_list[group_number].volunteer_time_needed:
                classroom_list[group_number].add_volunteer()