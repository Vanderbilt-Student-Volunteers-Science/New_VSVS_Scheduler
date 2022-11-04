from src.__init__ import MAX_TEAM_SIZE, partially_filled_classrooms, empty_classrooms, classroom_list, volunteer_list
from src.classroom import Classroom
from src.volunteer import Volunteer

#Assignments

def assign_partners(partner1):
    """
    Assigns a group of partners to a classroom they all can make (if there is one) using partner1.partner_schedule.
    When a group is assigned, uses classroom.assign_volunteer() for each partner (including partner1).


    :param partner1:the Volunteer object of the first partner in the group; the Volunteer object that contains the
                    information of the group of partners (only one is set when partners.csv is imported)
    :return:
    """
    classroom_idx = 0

    while partner1.group_number == -1 and classroom_idx < len(classroom_list):
        classroom = classroom_list[classroom_idx]
        if partners_can_make_class(partner1, classroom) and \
                MAX_TEAM_SIZE - classroom.volunteers_assigned >= partner1.partners + 1:
            classroom.assign_volunteer(partner1)
            for partner_index in partner1.partner_indexes:
                classroom.assign_volunteer(volunteer_list[partner_index])
        else:
            classroom_idx += 1
    if partner1.group_number == -1:
        print("WARNING: " + partner1.email + "'s partner group could not be assigned together because of scheduling "
                                             "conflicts.")


def assign_applied_t_leaders(sorted_t_leaders: list):
    """ Assigns team leaders to classroom groups that don't have them. Prioritizes assigning team leaders to
    partially-filled classroom groups over empty classroom groups.

    :param sorted_t_leaders: a list of unassigned volunteers that applied to be team leaders sorted from the fewest to
    the greatest number of classrooms they can make

    :return:
    """
    for t_leader in sorted_t_leaders:
        classroom_idx = 0

        while t_leader.group_number == -1 and classroom_idx < len(partially_filled_classrooms):
            classroom = partially_filled_classrooms[classroom_idx]
            if volunteer_can_make_class(t_leader, classroom) and not classroom.team_leader:
                classroom.assign_volunteer(t_leader)
                if classroom.volunteers_assigned >= MAX_TEAM_SIZE:
                    partially_filled_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while t_leader.group_number == -1 and classroom_idx < len(empty_classrooms):
            classroom = empty_classrooms[classroom_idx]
            if volunteer_can_make_class(t_leader, classroom):
                classroom.assign_volunteer(t_leader)
                partially_filled_classrooms.append(classroom)
                empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1


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


def volunteer_can_make_class(volunteer: Volunteer, classroom: Classroom):
    """ Returns boolean if volunteer can make a classroom.

    :param volunteer: Volunteer object of volunteer being checked
    :param classroom: Classroom object of classroom being checked
    :return:
    """
    return volunteer.free_time_array[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed


def partners_can_make_class(partner: Volunteer, classroom: Classroom):
    """ Returns boolean if a partner group can make a class.

    :param partner: Volunteer object of the first partner in the group; the Volunteer object that contains the
    information of the group of partners (only one is set when partners.csv is imported)
    :param classroom: Classroom object of classroom being checked
    :return:
    """
    return partner.partner_free_time_array[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed


# FIXME: Do we need these two methods? I feel like they can be done inline...
# Helper method for sort_by_availability
def return_classrooms_possible(volunteer):
    return volunteer.classrooms_possible


def sort_by_availability(volunteer_list: list):
    """ Sorts a list of Volunteer objects from the least to the greatest classrooms_possible

    :param volunteer_list:
    :return:
    """
    volunteer_list.sort(key=return_classrooms_possible)
    return volunteer_list
