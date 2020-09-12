import src.globalAttributes

# Assigns a group of partners to a classroom they all can make (if there is one) using the partner_schedule attribute of
# the first partner's Volunteer object. When a group is assigned, uses classroom.assign_volunteer to reflect this in the
# Volunteer objects of each of the volunteers in the group and the Classroom object of the classroom the group is being
# assigned to.
# partner1 - the Volunteer object of the first partner in the group; the Volunteer object that contains the information
#            of the group of partners (only one is set when partners.csv is imported)
def assign_partners(partner1):
    classroom_idx = 0

    while partner1.group_number == -1 and classroom_idx < len(src.globalAttributes.classroom_list):
        classroom = src.globalAttributes.classroom_list[classroom_idx]
        if partners_can_make_class(partner1, classroom) and src.globalAttributes.MAX_TEAM_SIZE - classroom.volunteers_assigned >= partner1.partners + 1:
            classroom.assign_volunteer(partner1)
            for partner_index in partner1.partner_indexes:
                classroom.assign_volunteer(src.globalAttributes.volunteer_list[partner_index])
        else:
            classroom_idx += 1
    if partner1.group_number == -1:
        print("WARNING: " + partner1.email + "'s partner group could not be assigned together because of scheduling conflicts.")


# Assigns drivers to classroom groups without drivers. If all of the classrooms a driver can make already have drivers
# (or are full), the driver is not assigned. When a driver is assigned, uses classroom.assign_volunteer to reflect this
# in the driver's Volunteer object and the Classroom object of the classroom they are being assigned to.
# sorted_drivers - list of all volunteers that are unassigned and can drive a group of volunteers sorted from the
#                  fewest to greatest number of classrooms they can make
def assign_in_person(sorted_in_person_volunteers):
    for volunteer in sorted_in_person_volunteers:
        classroom_idx = 0
        while volunteer.group_number == -1 and classroom_idx < len(src.globalAttributes.classroom_list):
            classroom = src.globalAttributes.classroom_list[classroom_idx]
            if volunteer_can_make_class(volunteer, classroom) and not classroom.has_in_person_volunteer and \
                    classroom.volunteers_assigned < src.globalAttributes.MAX_TEAM_SIZE:
                classroom.assign_volunteer(volunteer)
            else:
                classroom_idx += 1


# Assigns team leaders to classroom groups that don't have them. Prioritizes assigning team leaders to partially-filled
# classroom groups over empty classroom groups.
# sorted_applied_t_leaders - a list of unassigned volunteers that applied to be team leaders sorted from the fewest to
#                            greatest number of classrooms they can make
def assign_applied_t_leaders(sorted_t_leaders):
    for t_leader in sorted_t_leaders:
        classroom_idx = 0

        while t_leader.group_number == -1 and classroom_idx < len(src.globalAttributes.partially_filled_classrooms):
            classroom = src.globalAttributes.partially_filled_classrooms[classroom_idx]
            if volunteer_can_make_class(t_leader, classroom) and classroom.t_leader == 0:
                classroom.assign_volunteer(t_leader)
                if classroom.volunteers_assigned >= src.globalAttributes.MAX_TEAM_SIZE:
                    src.globalAttributes.partially_filled_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while t_leader.group_number == -1 and classroom_idx < len(src.globalAttributes.empty_classrooms):
            classroom = src.globalAttributes.empty_classrooms[classroom_idx]
            if volunteer_can_make_class(t_leader, classroom):
                classroom.assign_volunteer(t_leader)
                src.globalAttributes.partially_filled_classrooms.append(classroom)
                src.globalAttributes.empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1


# Assigns all unassigned volunteers to classroom groups. Prioritizes assigning each volunteer to a partially-filled
# classroom group over an empty classroom group.
# sorted_others - a list of unassigned volunteers sorted from the fewest to greatest number of classrooms they can make
def assign_others(sorted_others):
    for volunteer in sorted_others:
        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(src.globalAttributes.partially_filled_classrooms):
            classroom = src.globalAttributes.partially_filled_classrooms[classroom_idx]
            if volunteer_can_make_class(volunteer, classroom):
                classroom.assign_volunteer(volunteer)
                if classroom.volunteers_assigned >= src.globalAttributes.MAX_TEAM_SIZE:
                    src.globalAttributes.partially_filled_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1

        classroom_idx = 0

        while volunteer.group_number == -1 and classroom_idx < len(src.globalAttributes.empty_classrooms):
            if volunteer_can_make_class(volunteer, src.globalAttributes.empty_classrooms[classroom_idx]):
                src.globalAttributes.empty_classrooms[classroom_idx].assign_volunteer(volunteer)
                src.globalAttributes.partially_filled_classrooms.append(src.globalAttributes.empty_classrooms[classroom_idx])
                src.globalAttributes.empty_classrooms.pop(classroom_idx)
            else:
                classroom_idx += 1


# Returns boolean if volunteer can make a classroom.
# volunteer - Volunteer object of volunteer being checked
# classroom - Classroom object of classroom being checked
def volunteer_can_make_class(volunteer, classroom):
    return volunteer.free_time_array[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed


# Returns boolean if a partner group can make a class.
# partner -   Volunteer object of the first partner in the group; the Volunteer object that contains the information
#             of the group of partners (only one is set when partners.csv is imported)
# classroom - Classroom object of classroom being checked
def partners_can_make_class(partner, classroom):
    return partner.partner_free_time_array[classroom.start_time_schedule_index] >= classroom.volunteer_time_needed

# FIXME: Do we need these two methods? I feel like they can be done inline...
# Helper method for sort_by_availability
def return_classrooms_possible(volunteer):
    return volunteer.classrooms_possible


# Sorts a list of Volunteer objects from the least to greatest classrooms_possible
def sort_by_availability(volunteer_list):
    volunteer_list.sort(key=return_classrooms_possible)
    return volunteer_list