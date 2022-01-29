import csv
import os
import warnings

import src.assign
import src.classroom
import src.global_attributes
from src.classroom import Classroom
from src.global_attributes import VOLUNTEER_INDEX, CLASSROOM_INDEX
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
            # check that volunteer has vanderbilt email
            if not ('vanderbilt' in row[VOLUNTEER_INDEX['EMAIL']].strip().lower()):
                warnings.warn(
                    f"{row[VOLUNTEER_INDEX['FIRST']].strip()} {row[VOLUNTEER_INDEX['LAST']].strip()} does not have a Vanderbilt email.")

            # pull data from row in the csv, create a Volunteer object, and add it to global variable
            # volunteer_list
            # INDIVIDUAL_INDEX is a dictionary containing all the indices for each field
            volunteer = Volunteer(
                first=row[VOLUNTEER_INDEX['FIRST']].strip(),
                last=row[VOLUNTEER_INDEX['LAST']].strip(),
                phone=row[VOLUNTEER_INDEX['PHONE']].strip(),
                email=row[VOLUNTEER_INDEX['EMAIL']].strip().lower(),
                year_in_school=row[VOLUNTEER_INDEX['YEAR']].strip(),
                major=row[VOLUNTEER_INDEX['MAJOR']].strip(),
                applied_t_leader=(lambda x: True if x == 'Yes' else False)(
                    row[VOLUNTEER_INDEX['APPLIED_T_LEADER']].strip()),
                board=(lambda x: True if x == 'Yes' else False)(row[VOLUNTEER_INDEX['BOARD']].strip()),
                schedule=row[VOLUNTEER_INDEX['SCHEDULE_START']:VOLUNTEER_INDEX['SCHEDULE_END'] + 1]
            )
            src.global_attributes.volunteer_list.append(volunteer)

    print('There are {} volunteers.'.format(len(src.global_attributes.volunteer_list)))

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
        print('There are {} classes.'.format(len(src.global_attributes.classroom_list)))

    # ASSIGN VOLUNTEERS
    # First assign board members and their partners
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.board and volunteer.group_number == -1:
            src.assign.assign_single(volunteer)

    # print board members that cannot be assigned
    print("\n ------  BOARD MEMBERS THAT CANNOT BE ASSIGNED ------")
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.board and volunteer.group_number == -1:
            print(volunteer)
    print("-----------------------------------------------------")

    # count classrooms volunteers can make, total is Volunteer attribute classrooms_possible
    print("\nVolunteers removed due to incompatible schedules:\n")
    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1:
            for classroom in src.global_attributes.classroom_list:
                if src.assign.volunteer_can_make_class(volunteer, classroom):
                    volunteer.classrooms_possible += 1
            if not volunteer.classrooms_possible:
                print(volunteer)
                src.global_attributes.volunteer_list.remove(volunteer)
    print("-----------------------------------------------------\n")

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

    for volunteer in src.global_attributes.volunteer_list:
        if volunteer.group_number == -1:
            src.global_attributes.volunteer_list.remove(volunteer)

    # OUTPUT
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
                             "Year in School", "Major", "Team Leader"])

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
                    volunteer.major,
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


if __name__ == '__main__':
    main()
