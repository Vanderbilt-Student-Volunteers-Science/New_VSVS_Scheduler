from src.__init__ import MAX_TEAM_SIZE, partially_filled_classrooms, empty_classrooms, classroom_list, volunteer_list
from src.classroom import Classroom
from src.volunteer import Volunteer


def assign_others(sorted_others: list):
    """Assigns all unassigned volunteers to classroom groups. Prioritizes assigning each volunteer to a partially-filled
    classroom group over an empty classroom group.

    :param sorted_others: a list of unassigned volunteers sorted from the fewest to the greatest number of classrooms
    they can make
    :return:
    """
    for volunteer in sorted_others:
        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(partially_filled_classrooms):
            classroom = partially_filled_classrooms[classroom_idx]
            if volunteer_can_make_class(volunteer, classroom):
                classroom.assign_volunteer(volunteer)
                if classroom.volunteers_assigned >= MAX_TEAM_SIZE:
                    partially_filled_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(empty_classrooms):
            if volunteer_can_make_class(volunteer, empty_classrooms[classroom_idx]):
                empty_classrooms[classroom_idx].assign_volunteer(volunteer)
                partially_filled_classrooms.append(empty_classrooms[classroom_idx])
                empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1



