import csv
import os
import warnings

import src.assign
import src.classroom
import src.global_attributes
from src.classroom import Classroom
from src.global_attributes import INDIVIDUAL_INDEX, CLASSROOM_INDEX
from src.volunteer import Volunteer


# All global constants and variables are in global_attributes.py

def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return f"WARNING: {str(msg)}  \n"


warnings.formatwarning = custom_formatwarning


def main():
    #  IMPORT FILE DATA

    # import individual application data from individuals.csv
    with open('../data/individuals.csv', 'r') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # divides individuals_csv by commas
        next(csv_reader)  # skips the header
        for row in csv_reader:  # for each individual

            # check vanderbilt email
            if not ('vanderbilt' in row[INDIVIDUAL_INDEX['EMAIL']].strip().lower()):
                warnings.warn(
                    f"{row[INDIVIDUAL_INDEX['FIRST']].strip()} {row[INDIVIDUAL_INDEX['LAST']].strip()} does not have a Vanderbilt email.")

            # pull data from row in the csv, create a Volunteer object, and add it to global variable
            # volunteer_list
            # I is a dictionary containing all the indices for each field
            volunteer = Volunteer(
                first=row[INDIVIDUAL_INDEX['FIRST']].strip(),
                last=row[INDIVIDUAL_INDEX['LAST']].strip(),
                phone=row[INDIVIDUAL_INDEX['PHONE']].strip(),
                email=row[INDIVIDUAL_INDEX['EMAIL']].strip().lower(),
                year_in_school=row[INDIVIDUAL_INDEX['YEAR']].strip(),
                major=row[INDIVIDUAL_INDEX['MAJOR']].strip(),
                robotics_interest=False,  # no robotics for Spring 2021
                special_needs_interest=(lambda x: True if x == 'Yes' else False)(
                    row[INDIVIDUAL_INDEX['SPECIAL_NEEDS_INTEREST']].strip()),
                applied_t_leader=(lambda x: True if x == 'Yes' else False)(
                    row[INDIVIDUAL_INDEX['APPLIED_T_LEADER']].strip()),
                board=(lambda x: True if x == 'Yes' else False)(row[INDIVIDUAL_INDEX['BOARD']].strip()),
                driver=False,  # no drivers for Spring 2021
                car_passengers='',  # no drivers/cars for Spring 2021
                imported_schedule=row[INDIVIDUAL_INDEX['IMPORTED_SCHEDULE_START']:INDIVIDUAL_INDEX[
                                                                                      'IMPORTED_SCHEDULE_END'] + 1],
                # location column in csv is either 'On-campus' or 'Remote', so we need to convert to boolean
                is_in_person=(lambda x: True if x == 'On-campus' else False)(row[INDIVIDUAL_INDEX['LOCATION']].strip())
            )
            src.global_attributes.volunteer_list.append(volunteer)

    print('There are {} volunteers.'.format(len(src.global_attributes.volunteer_list)))

    # import partner application data from partners.csv

    with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # divides partners_csv by commas
        next(csv_reader)  # skip header row

        for row in csv_reader:  # for each group of partners
            first_partner_email = row[1].strip().lower()
            # if the first partner submitted an individual application
            if first_partner_email in [volunteer.email for volunteer in src.global_attributes.volunteer_list]:
                # find first partner
                for volunteer in src.global_attributes.volunteer_list:
                    if volunteer.email == first_partner_email:
                        first_partner = volunteer
                # add remaining partners to first partner
                first_partner.add_partners(*tuple(row[2:]))
            else:
                warnings.warn(f'{first_partner_email} filled out a partner application but not an individual '
                              f'application.')

    # import classroom information from classrooms.csv
    with open('../data/classrooms.csv', 'r') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # divides classrooms_csv by commas
        next(csv_reader)  # skip header row
        for row in csv_reader:  # for each classroom

            # creates a Classroom object and adds it to global variable classroom_list
            # row indices correspond to columns of classrooms.csv
            classroom = Classroom(group_number=int(row[CLASSROOM_INDEX['GROUP_NUMBER']].strip()),
                                  teacher_name=row[CLASSROOM_INDEX['TEACHER_NAME']].strip(),
                                  teacher_phone=row[CLASSROOM_INDEX['TEACHER_PHONE']].strip(),
                                  school=row[CLASSROOM_INDEX['SCHOOL']].strip(),
                                  teacher_email=row[CLASSROOM_INDEX['TEACHER_EMAIL']].strip(),
                                  class_start_time=row[CLASSROOM_INDEX['CLASS_START_TIME']].strip(),
                                  class_end_time=row[CLASSROOM_INDEX['CLASS_END_TIME']].strip(),
                                  day_of_week=row[CLASSROOM_INDEX['DAY_OF_WEEK']].strip()
                                  )

            src.global_attributes.classroom_list.append(classroom)

    # ASSIGN VOLUNTEERS

    # First assign board members and their partners
    # FIXME: this assumes all board members in groups are partner #1
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.board and volunteer.group_number == -1:
            if volunteer.partners:
                src.assign.assign_partners(volunteer)
                if volunteer.group_number == -1:
                    src.assign.assign_single(volunteer)
            else:
                src.assign.assign_single(volunteer)

    # print board members that can not be assigned
    print("\n ------  BOARD MEMBERS THAT CAN NOT BE ASSIGNED ------")
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.board and volunteer.group_number == -1:
            print(volunteer)
    print("------------")

    # assign partners
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.partners:
            src.assign.assign_partners(volunteer)  # adds all partners to same team

    # for unassigned volunteers, count classrooms they can make, total is Volunteer attribute classrooms_possible
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1:
            for classroom in src.global_attributes.classroom_list:
                if src.assign.volunteer_can_make_class(volunteer, classroom):
                    volunteer.classrooms_possible += 1

    # make list of unassigned in person volunteers, sort them by the number of classrooms they can make
    # (fewest to greatest number of classrooms they can make), then assign them to classroom groups
    in_person_list = []
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.is_in_person:
            in_person_list.append(volunteer)
    src.assign.assign_in_person(src.assign.sort_by_availability(in_person_list))

    # creates global variable lists of empty and partially filled classrooms
    for classroom in src.global_attributes.classroom_list:
        if classroom.volunteers_assigned == 0:
            src.global_attributes.empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < src.global_attributes.MAX_TEAM_SIZE:
            src.global_attributes.partially_filled_classrooms.append(classroom)

    # make list of unassigned applied_t_leaders, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    applied_t_leader_list = []
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1 and volunteer.applied_t_leader:
            applied_t_leader_list.append(volunteer)
    src.assign.assign_applied_t_leaders(src.assign.sort_by_availability(applied_t_leader_list))

    # make list of unassigned volunteers, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    unsorted_list = []
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    src.assign.assign_others(src.assign.sort_by_availability(unsorted_list))

    # reassign volunteers that were assigned to groups of 1
    # TODO: think through this part better
    # FIXME: catch ValueError from reassigning volunteers if we are going to do this
    unassigned_volunteers = []
    for classroom in src.global_attributes.classroom_list:
        if classroom.volunteers_assigned == 1:
            unassigned_volunteers.extend(classroom.empty_classroom())
    src.assign.assign_others(src.assign.sort_by_availability(unassigned_volunteers))

    # OUTPUT RESULTS

    unassigned_volunteers = 0

    # create the results directory if it does not exist
    path = "../results"

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            warnings.warn(f'failed to create {path} directory')
        else:
            print(f'Created {path} directory')

    with open('../results/raw_assignments.csv', 'w', newline='') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')

        # Header row
        csv_writer.writerow(["Volunteer ID", "Group Number", "First Name", "Last Name", "Email", "Phone Number",
                             "Year in School", " ", "Major", " ", "Driver", "Team Leader"])

        for volunteer_id, volunteer in enumerate(src.global_attributes.volunteer_list):
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

    for classroom in src.global_attributes.classroom_list:
        print("{} volunteers assigned to group {}".format(classroom.volunteers_assigned, classroom.group_number))

    classroom_counts = [0] * len(src.global_attributes.classroom_list)
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number != -1:
            classroom_counts[volunteer.group_number - 1] += 1

    print(classroom_counts)


# runs main
if __name__ == '__main__':
    main()
