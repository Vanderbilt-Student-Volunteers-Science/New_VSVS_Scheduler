# TODO: sort robotics?
# TODO: add global constants + change methods so scheduling times collected can be changed in the future (like constants for start time (7:15), time period (15 min), and periods collected (34))
# TODO: group_number == -1 means unassigned
# TODO: how many passengers to consider someone a driver? currently if passengers >= MAX_TEAM_SIZE. highest option on form is 4+, so if we change MAX_TEAM_SIZE to 5, no one will ever be a driver
# TODO: make sure all sorting stuff is pass by reference


import csv
import src.globalAttributes
import src.volunteer
import src.partners
import src.classroom
import src.assign
import src.convertSchedule


# row[2] is first name, row[3] is last name, row[4] is phone number, row[5] is email, row[7] is year, row[8] is major, row[9] is robotics interest,
# row[10] is special needs interest, row[12] is team leader interest, row[13] is previous team leader,
# row[15] is car passengers, row[16-49] are 15-min time slots that range from from 7:15am to 3:45pm


def main():

    #  IMPORT FILE DATA

    # import individual application data
    with open('../data/individuals.csv', 'r') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # csv_reader will divide individuals_csv by commas
        for row in csv_reader:

            # creates Volunteer objects and adds them to volunteer_list, indices correspond to columns of responses in
            # individuals.csv
            src.globalAttributes.volunteer_list.append(src.volunteer.Volunteer(row[2], row[3], row[4], row[5], row[7], row[8], row[9],
                                                          row[10], row[12], row[15],
                                                          src.convertSchedule.convert_to_schedule_array(row[16:50])))

    # probably don't need anymore (if we decide individuals and partners will share application)
    # import partner application data
    with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # csv_reader will divide partners_csv by commas
        for row in csv_reader:
            for volunteer in src.globalAttributes.volunteer_list:

                # adding partners to Volunteer object corresponding to volunteer that signed the group of partners up
                if volunteer.email == row[1]:
                    if len(row) == 5:
                        volunteer.add_partners(row[2], row[3], row[4])
                    elif len(row) == 4:
                        volunteer.add_partners(row[2], row[3], '')
                    else:
                        volunteer.add_partners(row[2], '', '')

    # import classroom information
    with open('../data/classrooms.csv', 'r') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # csv_reader will divide classrooms_csv by commas
        for row in csv_reader:
            # creates Classroom object
            src.globalAttributes.classroom_list.append(src.classroom.Classroom(row[1], row[3], row[4], row[6], row[9], row[11], row[12], row[13]))

    # set preassigned volunteers in classroom data before assigning
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number != -1:
            src.globalAttributes.classroom_list[volunteer.group_number].add_volunteer()


    # ASSIGN VOLUNTEERS

    # assign partners
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.partners:
            src.assign.assign_partners(volunteer)  # adds all partners to same team

    # for unassigned people, count classrooms they can make
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1:
            for classroom in src.globalAttributes.classroom_list:
                if src.assign.volunteer_can_make_class(volunteer, classroom):
                    volunteer.increment_classrooms_possible()

    # make driver list, sort by availability, assign drivers
    driver_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.driver:
            driver_list.append(volunteer)
    src.assign.assign_drivers(src.assign.sort_by_availability(driver_list))

    # creates lists of partially filled and empty classrooms
    empty_classrooms = []
    nonempty_classrooms = []
    for classroom in src.globalAttributes.classroom_list:
        if classroom.volunteers_assigned == 0:
            empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < src.globalAttributes.MAX_TEAM_SIZE:
            nonempty_classrooms.append(classroom)

    # assign unassigned applied_t_leaders AFTER sorting them by availability
    # (from fewest to most classrooms they can make)
    applied_t_leader_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.applied_t_leader:
            applied_t_leader_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(applied_t_leader_list), nonempty_classrooms, empty_classrooms)

    # assign everyone else still unassigned AFTER sorting them by availability
    # (from fewest to most classrooms they can make)
    unsorted_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(unsorted_list), nonempty_classrooms, empty_classrooms)


    # OUTPUT RESULTS

    with open('../results/assignments.csv', 'w') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        for volunteer_id in range(len(src.globalAttributes.volunteer_list)):
            csv_writer.writerow(
                [volunteer_id, src.globalAttributes.volunteer_list[volunteer_id].group_number, src.globalAttributes.volunteer_list[volunteer_id].first,
                 src.globalAttributes.volunteer_list[volunteer_id].last, src.globalAttributes.volunteer_list[volunteer_id].email,
                 src.globalAttributes.volunteer_list[volunteer_id].phone, src.globalAttributes.volunteer_list[volunteer_id].year_in_school,
                 '', src.globalAttributes.volunteer_list[volunteer_id].major, '', src.globalAttributes.volunteer_list[volunteer_id].assigned_driver,
                 src.globalAttributes.volunteer_list[volunteer_id].assigned_t_leader])


# runs main
if __name__ == '__main__':
    main()
