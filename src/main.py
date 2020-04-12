# TODO: sort robotics?
# TODO: add global constants + change methods so scheduling times collected can be changed in the future (like constants for start time (7:15), time period (15 min), and periods collected (34))
# TODO: group_number == -1 means unassigned
# TODO: how many passengers to consider someone a driver? currently if passengers >= MAX_TEAM_SIZE. highest option on form is 4+, so if we change MAX_TEAM_SIZE to 5, no one will ever be a driver

# VSVS Volunteer Sorting Program, created 2019-2020
# Imports data from data/classrooms.csv, data/individuals.csv, and data/partners.csv and assigns volunteers to groups. Assigns
# partners, then drivers, then team leaders, then everyone else. Outputs results in results/assignments.csv.

# Before running:
#   1. Export the responses to the individual application to csv and call it individuals.csv
#   2. Export the responses to the partner application to csv and call it partners.csv
#   3. Copy and paste (don't export) the classroom table from Access and call it classrooms.csv
#   4. Delete the heading row from all three tables (so that the first row in each table is the first row of data)
#   5. Place individuals.csv, partners.csv, and classrooms.csv into the data directory of this program
#   6. Create a new file in the results directory called assignments.csv (where the program will write results)

# Columns of individuals.csv that matter (using zero-based indexing):
#   column 2 is first name
#   column 3 is last name
#   column 4 is phone number
#   column 5 is email
#   column 6 is year
#   column 8 is major
#   column 9 is robotics interest
#   column 10 is special needs interest
#   column 12 is team leader interest
#   column 13 is previous team leader
#   column 15 is car passengers
#   columns 16-49 are 15-min time slots that range from from 7:15am to 3:45pm; values are the days of the week a
#                 volunteer is busy during the time indicated by the column

# partners.csv contains the email addresses of the people that applied to be partners

# Columns of classrooms.csv that matter (using zero-based indexing):
#   column 1 is group number
#   column 3 is teacher name
#   column 4 is teacher phone
#   column 6 is school name
#   column 9 is teacher email
#   column 11 is class start time
#   column 12 is class end time
#   column 13 is day of week of the class

# Columns of assignments.csv (formatted for Access):
#   column 0 is volunteer id
#   column 1 is group number
#   column 2 is first name
#   column 3 is last name
#   column 4 is email
#   column 5 is phone number
#   column 6 is year in school
#   column 8 is major
#   column 10 is if they are assigned to be a driver
#   column 11 is if they are assigned to be a team leader


import csv
import src.globalAttributes
import src.volunteer
import src.partners
import src.classroom
import src.assign
import src.convertSchedule

# All global constants and variables are in globalAttributes.py


def main():

    #  IMPORT FILE DATA

    # import individual application data from individuals.csv
    with open('../data/individuals.csv', 'r') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # divides individuals_csv by commas
        for row in csv_reader:  # for each individual

            # creates a Volunteer object and adds it to global variable volunteer_list
            # row indices correspond to columns of responses in individuals.csv
            src.globalAttributes.volunteer_list.append(src.volunteer.Volunteer(row[2], row[3], row[4], row[5], row[7],
                                                                               row[8], row[9], row[10], row[12], row[15],
                                                                               src.convertSchedule.convert_to_schedule_array(row[16:50])))

    # import partner application data from partners.csv
    with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # divides partners_csv by commas
        for row in csv_reader:  # for each group of partners

            # finds first volunteer in partner group in volunteer_list and sets their Volunteer object
            # attributes partners, partner_indexes, and partner_schedule
            for volunteer in src.globalAttributes.volunteer_list:
                if volunteer.email == row[1]:
                    if len(row) == 5:
                        volunteer.add_partners(row[2], row[3], row[4])
                    elif len(row) == 4:
                        volunteer.add_partners(row[2], row[3], '')
                    else:
                        volunteer.add_partners(row[2], '', '')

    # import classroom information from classrooms.csv
    with open('../data/classrooms.csv', 'r') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # divides classrooms_csv by commas
        for row in csv_reader:  # for each classroom

            # creates a Classroom object and adds it to global variable classroom_list
            # row indices correspond to columns of classrooms.csv
            src.globalAttributes.classroom_list.append(src.classroom.Classroom(row[1], row[3], row[4], row[6], row[9],
                                                                               row[11], row[12], row[13]))


    # ASSIGN VOLUNTEERS

    # assign partners
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.partners:
            src.assign.assign_partners(volunteer)  # adds all partners to same team

    # for unassigned volunteers, count classrooms they can make, total is Volunteer attribute classrooms_possible
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1:
            for classroom in src.globalAttributes.classroom_list:
                if src.assign.volunteer_can_make_class(volunteer, classroom):
                    volunteer.increment_classrooms_possible()

    # make list of unassigned drivers, sort them by the number of classrooms they can make (fewest to greatest number
    # of classrooms they can make), then assign them to classroom groups
    driver_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.driver:
            driver_list.append(volunteer)
    src.assign.assign_drivers(src.assign.sort_by_availability(driver_list))

    # creates lists of empty and partially filled classrooms
    empty_classrooms = []
    partially_filled_classrooms = []
    for classroom in src.globalAttributes.classroom_list:
        if classroom.volunteers_assigned == 0:
            empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < src.globalAttributes.MAX_TEAM_SIZE:
            partially_filled_classrooms.append(classroom)

    # make list of unassigned applied_t_leaders, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    applied_t_leader_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.applied_t_leader:
            applied_t_leader_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(applied_t_leader_list), partially_filled_classrooms, empty_classrooms)

    # make list of unassigned volunteers, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    unsorted_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    src.assign.assign_group(src.assign.sort_by_availability(unsorted_list), partially_filled_classrooms, empty_classrooms)


    # OUTPUT RESULTS

    with open('../results/assignments.csv', 'w') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        for volunteer_id in range(len(src.globalAttributes.volunteer_list)):
            csv_writer.writerow(
                [volunteer_id, src.globalAttributes.volunteer_list[volunteer_id].group_number,
                 src.globalAttributes.volunteer_list[volunteer_id].first,
                 src.globalAttributes.volunteer_list[volunteer_id].last,
                 src.globalAttributes.volunteer_list[volunteer_id].email,
                 src.globalAttributes.volunteer_list[volunteer_id].phone,
                 src.globalAttributes.volunteer_list[volunteer_id].year_in_school, '',
                 src.globalAttributes.volunteer_list[volunteer_id].major, '',
                 src.globalAttributes.volunteer_list[volunteer_id].assigned_driver,
                 src.globalAttributes.volunteer_list[volunteer_id].assigned_t_leader])


# runs main
if __name__ == '__main__':
    main()
