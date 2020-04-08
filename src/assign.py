import src.volunteer
import src.classroom
import src.globalAttributes


# adds all partners to same team
# TODO

def assign_partners(partner):
    classroom_idx = 0

    while partner.group_number == -1 and classroom_idx < len(src.globalAttributes.classroom_list):
        classroom = src.globalAttributes.classroom_list[classroom_idx]
        if partners_can_make_class(partner, classroom) and src.globalAttributes.MAX_TEAM_SIZE - classroom.volunteers_assigned >= partner.partners + 1:
            classroom.assign_volunteer(partner)
            for partner_index in partner.partner_indexes:
                classroom.assign_volunteer(src.globalAttributes.volunteer_list[partner_index])
        else:
            classroom_idx += 1


def assign_drivers(sorted_driver_list):
    for driver in sorted_driver_list:
        classroom_idx = 0
        while driver.group_number == -1 and classroom_idx < len(src.globalAttributes.classroom_list):
            classroom = src.globalAttributes.classroom_list[classroom_idx]
            if volunteer_can_make_class(driver, classroom) and classroom.driver == 0 and classroom.volunteers_assigned < src.globalAttributes.MAX_TEAM_SIZE:
                classroom.assign_volunteer(driver)
            else:
                classroom_idx += 1


# Matches people in an input list ("subgroup") to a classroom they can make. Subgroup can be list of drivers, t_leaders,
# or others. If group is t_leaders or others the list will be sorted from lowest to highest availability.
# TODO: Tries to match person with partially filled classrooms first. If they can't make any partially filled
#  classrooms, try to place them in an classroom with no volunteers (yet).
def assign_group(sorted_subgroup, nonempty_classrooms, empty_classrooms):
    for volunteer in sorted_subgroup:
        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(nonempty_classrooms):
            classroom = nonempty_classrooms[classroom_idx]
            if volunteer_can_make_class(volunteer, classroom):
                classroom.assign_volunteer(volunteer)
                if classroom.volunteers_assigned >= src.globalAttributes.MAX_TEAM_SIZE:
                    nonempty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(empty_classrooms):
            if volunteer_can_make_class(volunteer, empty_classrooms[classroom_idx]):
                empty_classrooms[classroom_idx].assign_volunteer(volunteer)
                nonempty_classrooms.append(empty_classrooms[classroom_idx])
                empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1
    return

# boolean if volunteer can make a class
def volunteer_can_make_class(volunteer, classroom):
    return volunteer.schedule[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed

def partners_can_make_class(partner, classroom):
    return partner.partner_schedule[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed

def return_classrooms_possible(volunteer):
    return volunteer.classrooms_possible

def sort_by_availability(list):
    list.sort(key=return_classrooms_possible)
    return list