import warnings

import src.global_attributes
from src.classroom import Classroom
from src.volunteer import Volunteer


def assign(sorted_in_person_volunteers):
    """Assigns drivers to classroom groups without drivers. If all of the classrooms a driver can make already have
    drivers (or are full), the driver is not assigned. When a driver is assigned, uses classroom.assign_volunteer to
    reflect this in the driver's Volunteer object and the Classroom object of the classroom they are being assigned to.

    :param sorted_in_person_volunteers: list of all volunteers that are unassigned and can drive a group of
    volunteers sorted from the fewest to greatest number of classrooms they can make
    :type sorted_in_person_volunteers: list[Volunteer]
    :return: None
    """
    for volunteer in sorted_in_person_volunteers:
        classroom_idx = 0
        while volunteer.group_number == -1 and classroom_idx < len(src.global_attributes.classroom_list):
            classroom = src.global_attributes.classroom_list[classroom_idx]
            if volunteer_can_make_class(volunteer, classroom) and not classroom.has_in_person_volunteer and \
                    classroom.volunteers_assigned < src.global_attributes.MAX_TEAM_SIZE:
                classroom.assign_volunteer(volunteer)
            else:
                classroom_idx += 1


# TODO: fix syntax of loops (for classroom in classroom list)
def assign_applied_t_leaders(sorted_t_leaders):
    """ Assigns team leaders to classroom groups that don't have them. Prioritizes assigning team leaders to
    partially-filled classroom groups over empty classroom groups.

    :param sorted_t_leaders: a list of unassigned volunteers that applied to be team leaders sorted from the fewest
    to greatest number of classrooms they can make
    :type sorted_t_leaders: list[Volunteer]
    :return:
    """
    for t_leader in sorted_t_leaders:
        classroom_idx = 0

        while t_leader.group_number == -1 and classroom_idx < len(src.global_attributes.partially_filled_classrooms):
            classroom = src.global_attributes.partially_filled_classrooms[classroom_idx]
            if volunteer_can_make_class(t_leader, classroom) and classroom.t_leader == 0:
                classroom.assign_volunteer(t_leader)
                if classroom.volunteers_assigned >= src.global_attributes.MAX_TEAM_SIZE:
                    src.global_attributes.partially_filled_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while t_leader.group_number == -1 and classroom_idx < len(src.global_attributes.empty_classrooms):
            classroom = src.global_attributes.empty_classrooms[classroom_idx]
            if volunteer_can_make_class(t_leader, classroom):
                classroom.assign_volunteer(t_leader)
                src.global_attributes.partially_filled_classrooms.append(classroom)
                src.global_attributes.empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1


# TODO: fix syntax of loops (for classroom in classroom list)
def assign_others(sorted_others):
    """ Assigns all unassigned volunteers to classroom groups. Prioritizes assigning each volunteer to a
    partially-filled classroom group over an empty classroom group.

    :param sorted_others: a list of unassigned volunteers sorted from the fewest to greatest number of classrooms they can make
    :type sorted_others: list[Volunteer]
    :return:
    """
    for volunteer in sorted_others:
        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(src.global_attributes.partially_filled_classrooms):
            classroom = src.global_attributes.partially_filled_classrooms[classroom_idx]
            if volunteer_can_make_class(volunteer, classroom):
                classroom.assign_volunteer(volunteer)
                if classroom.volunteers_assigned >= src.global_attributes.MAX_TEAM_SIZE:
                    src.global_attributes.partially_filled_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(src.global_attributes.empty_classrooms):
            if volunteer_can_make_class(volunteer, src.global_attributes.empty_classrooms[classroom_idx]):
                src.global_attributes.empty_classrooms[classroom_idx].assign_volunteer(volunteer)
                src.global_attributes.partially_filled_classrooms.append(
                    src.global_attributes.empty_classrooms[classroom_idx])
                src.global_attributes.empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1


def volunteer_can_make_class(volunteer, classroom):
    """ Returns boolean if volunteer can make a classroom.

    :param volunteer: Volunteer object of volunteer being checked
    :type volunteer: Volunteer
    :param classroom: Classroom object of classroom being checked
    :type classroom: Classroom
    :return: if volunteer can make a classroom
    :rtype: bool
    """
    return volunteer.free_time_array[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed


# FIXME: Do we need these two methods? I feel like they can be done inline...
def return_classrooms_possible(volunteer):
    """ Helper method for sort_by_availability

    :param volunteer:
    :type volunteer: Volunteer
    :return: number of classrooms possible
    """
    return volunteer.classrooms_possible


def sort_by_availability(volunteer_list):
    """ Sorts a list of Volunteer objects from the least to greatest classrooms_possible

    :param volunteer_list: list of volunteers
    :type volunteer_list: list[Volunteer]
    :return: sorted volunteer list
    :rtype: list[Volunteer]
    """
    volunteer_list.sort(key=return_classrooms_possible)
    return volunteer_list


def assign_single(volunteer):
    """ assigns a single volunteer to first available classroom

    :param volunteer: volunteer to be assignees
    :type volunteer: Volunteer
    :return:
    """
    # loop through classrooms
    for classroom in src.global_attributes.classroom_list:
        if volunteer.group_number == -1:
            # assign to first classroom the volunteer can make
            if src.assign.volunteer_can_make_class(volunteer, classroom):
                classroom.assign_volunteer(volunteer)
        else:
            return
