# TODO: sort robotics?
# TODO: group_number == -1 means unassigned

import csv
import src.volunteer
import src.partners
import src.classroom
import src.assign

MAX_TEAM_SIZE = 4
MIN_TEAM_SIZE = 4


# TODO: add what row index inputs correspond to

volunteer_list = []  # list of all the volunteers that will be iterated through
classroom_list = []  # list of all the classrooms to to assign groups to

def main():



    #  IMPORT FILE DATA

    # import individual application data
    with open('../data/individuals.csv') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # csv_reader will divide individuals_csv by commas
        for row in csv_reader:
            # creates Volunteer objects and adds them to volunteer_list, indices correspond to columns of responses in
            # volunteers.csv
            volunteer_list.append(src.volunteer.Volunteer(row[0])) # TODO: add row indexes corresponding to csv output of new form

    # probably don't need anymore (if we decide individuals and partners will share application)
    # # import partner application data
    # with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
    #     csv_reader = csv.reader(partners_csv, delimiter=',')  # csv_reader will divide partners_csv by commas
    #     for row in csv_reader:
    #         volunteer_list[row[1]].add_partners(row[2], row[3], row[4], row[6])  # calling addPartner method on line of volunteer that signed partners up (volunteer_list[row[1]])

    # import classroom information
    with open('../data/classrooms.csv') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # csv_reader will divide classrooms_csv by commas
        for row in csv_reader:
            # creates Classroom object
            classroom_list.append(src.classroom.Classroom(row[2], row[3], row[4], row[6], row[9], row[11], row[12], row[13]))

    # set preassigned volunteers in classroom data before assigning
    for volunteer in volunteer_list:
        if volunteer.group_number != -1:
            classroom_list[volunteer.group_number].add_volunteer()


    # ASSIGN VOLUNTEERS

    # assign partners
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.partners:
            src.assign.assign_partners(volunteer)  # adds all partners to same team

    # assign drivers
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.car_passengers >= MIN_TEAM_SIZE:  # figure this out: keep their group under car capacity or don't allow car unless it is TEAM_MAX_MEMBERS
            src.assign.assign_group(driver_list, classroom_list)

    # for unassigned people, count classrooms they can make
    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            for classroom in classroom_list:
                if src.assign.volunteer_can_make_class(volunteer, classroom):
                    volunteer.increment_classrooms_possible()

    # creates lists of partially filled and empty classrooms
    empty_classrooms = []
    nonempty_classrooms = []
    for classroom in classroom_list:
        if classroom.volunteers_assigned == 0:
            empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < MAX_TEAM_SIZE:
            nonempty_classrooms.append(classroom)

    # assign unassigned applied_t_leaders AFTER sorting them by availability
    # (from fewest to most classrooms they can make)
    applied_t_leader_list = []
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.applied_t_leader:
            applied_t_leader_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(applied_t_leader_list), classroom_list)

    # TODO: copy results of group assignments from applied_t_leader_list to volunteer_list

    # assign everyone else still unassigned AFTER sorting them by availability
    # (from fewest to most classrooms they can make)
    unsorted_list = []
    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(unsorted_list), classroom_list)

    # TODO: copy results of group assignments from unsorted_list to volunteer_list


    # OUTPUT RESULTS

    with open('../results/assignments.csv') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        for volunteer_id in range(1, len(volunteer_list)):
            csv_writer.writerow(
                [volunteer_id, volunteer_list[volunteer_id].group_number, volunteer_list[volunteer_id].first,
                 volunteer_list[volunteer_id].last, volunteer_list[volunteer_id].email,
                 volunteer_list[volunteer_id].phone])


# runs main
if __name__ == "__main__":
    main()
