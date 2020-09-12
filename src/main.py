# TO DO FUTURE
# TODO: sort robotics?
# TODO: add global constants + change methods so scheduling times collected can be changed in the future (like constants for start time (7:15), time period (15 min), and periods collected (34))
# TODO: group_number == -1 means unassigned
# TODO: how many passengers to consider someone a driver? currently if passengers >= MAX_TEAM_SIZE. highest option on form is 4+, so if we change MAX_TEAM_SIZE to 5, no one will ever be a driver
# TODO: optimize scheduling more by adding TRAVEL_TIME constants for every school

# Possible TO Do
# TODO: The phone numbers have different formats. We could use this package: https://pypi.org/project/phonenumbers/
#  to parse phone numbers

# TESTING METRICS
# people can make classrooms they're assigned to
# groups are assigned together - yes
# each group has at least one in-person - yes
# see how many groups of <MAX there are

# VSVS Volunteer Sorting Program, created 2019-2020
# Imports data from data/classrooms.csv, data/individuals.csv, and data/partners.csv and assigns volunteers to groups. Assigns
# partners, then drivers, then team leaders, then everyone else. Outputs results in results/assignments.csv.

# Before running:
#   1. Export the responses to the individual application to csv and call it individuals.csv
#   2. Export the responses to the partner application to csv and call it partners.csv
#   3. Copy and paste (don't export) the classroom table from Access with headings and call it classrooms.csv
#   4. Place individuals.csv, partners.csv, and classrooms.csv into the data directory of this program

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
import os

import src.assign
import src.classroom
import src.globalAttributes
from src.classroom import Classroom
from src.globalAttributes import I
from src.volunteer import Volunteer


# All global constants and variables are in globalAttributes.py


def main():
    #  IMPORT FILE DATA

    # import individual application data from individuals.csv
    with open('../data/individuals.csv', 'r') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # divides individuals_csv by commas
        next(csv_reader)  # skips the header
        for row in csv_reader:  # for each individual

            # pull data from row in the csv, create a Volunteer object, and add it to global variable
            # volunteer_list
            # I is a dictionary containing all the indices for each field
            volunteer = Volunteer(
                first=row[I['FIRST']].strip(),
                last=row[I['LAST']].strip(),
                phone=row[I['PHONE']].strip(),
                email=row[I['EMAIL']].strip(),
                year_in_school=row[I['YEAR']].strip(),
                major=row[I['MAJOR']].strip(),
                robotics_interest=False,  # no robotics for Fall 2020
                special_needs_interest=(lambda x: True if x == 'Yes' else False)(row[I['SPECIAL_NEEDS_INTEREST']].strip()),
                applied_t_leader=(lambda x: True if x == 'Yes' else False)(row[I['APPLIED_T_LEADER']].strip()),
                car_passengers=0,  # no drivers/cars for Fall 2020
                imported_schedule=row[I['IMPORTED_SCHEDULE_START']:I['IMPORTED_SCHEDULE_END'] + 1],
                # location column in csv is either 'On-campus' or 'Remote', so we need to convert to boolean
                is_in_person=(lambda x: True if x == 'On-campus' else False)(row[I['LOCATION']].strip())
            )
            src.globalAttributes.volunteer_list.append(volunteer)

    print('There are {} volunteers.'.format(len(src.globalAttributes.volunteer_list)))

    # import partner application data from partners.csv
    with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # divides partners_csv by commas
        next(csv_reader) # skip header row
        for row in csv_reader:  # for each group of partners

            # finds first volunteer in partner group in volunteer_list and sets their Volunteer object
            # attributes partners, partner_indexes, and partner_schedule
            volunteer_index = 0
            first_volunteer_matched = 0
            while volunteer_index < len(src.globalAttributes.volunteer_list) and first_volunteer_matched == 0:
                volunteer = src.globalAttributes.volunteer_list[volunteer_index]
                volunteer_index += 1
                if row[1].lower() == volunteer.email:
                    if len(row) == 5:
                        volunteer.add_partners(row[2], row[3], row[4])
                    elif len(row) == 4:
                        volunteer.add_partners(row[2], row[3], '')
                    else:
                        volunteer.add_partners(row[2], '', '')
                    first_volunteer_matched = 1

                # if no volunteers in volunteer_list have same email, print an alert
                elif volunteer == src.globalAttributes.volunteer_list[-1]:
                    print('WARNING: ' + row[1] + ' first volunteer in their partner group was not found in individual application data.')

    # import classroom information from classrooms.csv
    with open('../data/classrooms.csv', 'r') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # divides classrooms_csv by commas
        next(csv_reader)  # skip header row
        for row in csv_reader:  # for each classroom

            # creates a Classroom object and adds it to global variable classroom_list
            # row indices correspond to columns of classrooms.csv
            classroom = Classroom(group_number=int(row[1].strip()),
                                  teacher_name=row[3],
                                  teacher_phone=row[4],
                                  school=row[6],
                                  teacher_email=row[9],
                                  class_start_time=row[11],
                                  class_end_time=row[12],
                                  day_of_week=row[13]
                                  )
            src.globalAttributes.classroom_list.append(classroom)

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

    # make list of unassigned in person volunteers, sort them by the number of classrooms they can make
    # (fewest to greatest number of classrooms they can make), then assign them to classroom groups
    in_person_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.is_in_person:
            in_person_list.append(volunteer)
    src.assign.assign_in_person(src.assign.sort_by_availability(in_person_list))

    # creates global variable lists of empty and partially filled classrooms
    for classroom in src.globalAttributes.classroom_list:
        if classroom.volunteers_assigned == 0:
            src.globalAttributes.empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < src.globalAttributes.MAX_TEAM_SIZE:
            src.globalAttributes.partially_filled_classrooms.append(classroom)

    # make list of unassigned applied_t_leaders, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    applied_t_leader_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.applied_t_leader:
            applied_t_leader_list.append(volunteer)
    src.assign.assign_applied_t_leaders(src.assign.sort_by_availability(applied_t_leader_list))

    # make list of unassigned volunteers, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    unsorted_list = []
    for volunteer in src.globalAttributes.volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    src.assign.assign_others(src.assign.sort_by_availability(unsorted_list))

    # OUTPUT RESULTS

    unassigned_volunteers = 0

    # create the results directory if it does not exist
    path = "../results"

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print('WARNING: failed to create {} directory'.format(path))
        else:
            print('Created {} directory'.format(path))
    else:
        print('{} directory already exists'.format(path))

    with open('../results/assignments.csv', 'w', newline='') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        # FIXME: should we add a header row for this output file?
        for volunteer_id, volunteer in enumerate(src.globalAttributes.volunteer_list):
            if volunteer.group_number == -1:
                unassigned_volunteers += 1
            csv_writer.writerow(
                [
                    volunteer_id,
                    volunteer.group_number,
                    volunteer.first,
                    volunteer.last,
                    volunteer.email,
                    volunteer.phone,
                    volunteer.year_in_school,
                    '',
                    volunteer.major,
                    '',
                    int(volunteer.assigned_driver),  # convert True/False to 1/0
                    int(volunteer.assigned_t_leader)  # convert True/False to 1/0
                ]
            )

    print('There were {} unassigned volunteers.'.format(unassigned_volunteers))


# runs main
if __name__ == '__main__':
    main()
