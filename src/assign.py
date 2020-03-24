import src.volunteer
import src.classroom


# TODO: deal with t_leaders and drivers (only want to assign one)

class Assign:

    # assign through people from least to most available
    # assign volunteers to partially filled groups before an empty group
    # for each person, iterate them through array of partially filled then array of empty classrooms

    def findClassroom(mode, volunteer, classroom_list):
        if mode == 'partners':
            for group_number in range(1, len(classroom_list)):
                if volunteer.partner_details.partner_schedule[classroom_list[group_number].start_time_schedule_index] >= classroom_list[group_number].volunteer_time_needed:
                    assign_volunteer(volunteer, group_number)
                    for partner_number in range(1, volunteer.partners):  # one-based indexing
                        assign_volunteer(volunteer_list[volunteer.partner_details.partner[partner_number]], group_number)
                        return
        elif mode == 'drivers':
        elif mode == 't_leaders':

            if (classroom_list[group_number].volunteers_assigned > MIN_TEAM_SIZE):

            if 
                if volunteer.schedule[classroom_list[group_number].start_time_schedule_index] >= classroom_list[group_number].volunteer_time_needed:
                    classroom_list[group_number].add_volunteer()

                """ if class is above min
                        if if they can be assigned to another group, assign them, if not, and group below max, assign to   """