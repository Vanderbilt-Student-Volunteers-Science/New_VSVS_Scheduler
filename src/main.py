import csv
import os

from src.assign import assign_partners, volunteer_can_make_class,  sort_by_availability, \
    assign_applied_t_leaders, assign_others
import src.classroom
import src.globalAttributes
from src.classroom import Classroom
from src.volunteer import Volunteer
from src.__init__ import volunteer_list, classroom_list


# All global constants and variables are in globalAttributes.py (If we included them in here, it would result in
# circular imports)

def main():
    #  IMPORT FILE DATA

    # import individual application data from individuals.csv
    with open('../data/individuals.csv', 'r') as individuals_csv:  # opens individuals.csv as individuals_csv
        # returns each row in the csv as a dictionary. The first row in the csv is used for the keys of the dictionary
        csv_reader = csv.DictReader(individuals_csv)

        for row in csv_reader:  # for each individual
            # pull data from row in the csv, create a Volunteer object, and add it to global variable volunteer_list

            volunteer = Volunteer(
                first=row['First Name'].strip(),
                last=row['Last Name'].strip(),
                phone=row['Phone Number'],
                email=row['Email'].strip(),
                robotics_interest=False,  # no robotics for Fall 2020
                special_needs_interest=(lambda x: True if x == 'Yes' else False)(
                    row['Special Needs Students']),
                leader_app=(lambda x: True if x == 'Yes' else False)(row['Team Leader']),
                imported_schedule=list(row.values())[16:50],
            )
            volunteer_list.append(volunteer)

    print('There are {} volunteers.'.format(len(volunteer_list)))

    # import partner application data from partners.csv
    with open('../data/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # divides partners_csv by commas
        next(csv_reader)  # skip header row
        for row in csv_reader:  # for each group of partners

            # finds first volunteer in partner group in volunteer_list and sets their Volunteer object
            # attributes partners, partner_indexes, and partner_schedule
            volunteer_index = 0
            first_volunteer_matched = 0
            while volunteer_index < len(volunteer_list) and first_volunteer_matched == 0:
                volunteer = volunteer_list[volunteer_index]
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
                elif volunteer == volunteer_list[-1]:
                    print('WARNING: ' + row[
                        1] + ' first volunteer in their partner group was not found in individual application data.')

    # import classroom information from classrooms.csv
    with open('../data/classrooms.csv', 'r') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.DictReader(classrooms_csv)
        for row in csv_reader:  # for each teacher application
            teacher_name = row['Name']
            teacher_phone = row['Cell Phone Number']
            school = row['School']
            email = row['Email Address']
            number_of_classes = row['Number of Classes']
            for i in range(int(number_of_classes)): # for all of that teacher's classes
                # class_num keeps track of which class out of the total number_of_classes is being created
                class_num = i + 1
                # creates a Classroom object and adds it to global variable classroom_list
                classroom = Classroom(group_number=1,
                                      teacher_name=teacher_name,
                                      teacher_phone=teacher_phone,
                                      school=school,
                                      teacher_email=email,
                                      class_start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                                      class_end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                                      day_of_week='Thursday'
                                      )
            classroom_list.append(classroom)

    # ASSIGN VOLUNTEERS

    # assign partners
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.partners:
            assign_partners(volunteer)  # adds all partners to same team

    # for unassigned volunteers, count classrooms they can make, total is Volunteer attribute classrooms_possible
    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            for classroom in classroom_list:
                if volunteer_can_make_class(volunteer, classroom):
                    volunteer.increment_classrooms_possible()

    # creates global variable lists of empty and partially filled classrooms
    for classroom in classroom_list:
        if classroom.volunteers_assigned == 0:
            src.globalAttributes.empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < src.globalAttributes.MAX_TEAM_SIZE:
            src.globalAttributes.partially_filled_classrooms.append(classroom)

    # make list of unassigned applied_t_leaders, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    applied_t_leader_list = []
    for volunteer in volunteer_list:
        if volunteer.group_number == -1 and volunteer.leader_app:
            applied_t_leader_list.append(volunteer)
    assign_applied_t_leaders(sort_by_availability(applied_t_leader_list))

    # make list of unassigned volunteers, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)
    unsorted_list = []
    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            unsorted_list.append(volunteer)
    assign_others(sort_by_availability(unsorted_list))

    # reassign volunteers that were assigned to groups of 1
    # TODO: think through this part better
    unassigned_volunteers = []
    for classroom in classroom_list:
        if classroom.volunteers_assigned == 1:
            unassigned_volunteers.extend(classroom.empty_classroom())
    assign_others(sort_by_availability(unassigned_volunteers))

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

    group_size = [0] * 108
    with open('../results/assignments.csv', 'w', newline='') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        # FIXME: should we add a header row for this output file?
        for volunteer_id, volunteer in enumerate(volunteer_list):
            if volunteer.group_number == -1:
                unassigned_volunteers += 1
            else:
                group_size[volunteer.group_number] += 1
            csv_writer.writerow(
                [
                    volunteer_id,
                    volunteer.group_number,
                    volunteer.first,
                    volunteer.last,
                    volunteer.email,
                    volunteer.phone,
                    '',
                    '',
                    int(volunteer.assigned_driver),  # convert True/False to 1/0
                    int(volunteer.assigned_t_leader)  # convert True/False to 1/0
                ]
            )

    print('There were {} unassigned volunteers.'.format(unassigned_volunteers))

    # TODO: Remove after testing?
    for classroom in classroom_list:
        print("{} volunteers assigned to group {}".format(group_size[classroom.group_number], classroom.group_number))


# runs main
if __name__ == '__main__':
    main()
