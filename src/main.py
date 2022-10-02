import csv
import os

from src.assign import assign_partners, volunteer_can_make_class, sort_by_availability, \
    assign_applied_t_leaders, assign_others
from src.classroom import Classroom
from src.volunteer import Volunteer, import_volunteers, import_partners
from src.__init__ import volunteer_list, partially_filled_classrooms, empty_classrooms, MAX_TEAM_SIZE, classroom_list


# All global constants and variables are in __init__.py (If we included them in here, it would result in
# circular imports and )

def main():
    #  IMPORT FILE DATA
    import_volunteers('../data/individuals.csv')  # import volunteer application data from volunteers.csv
    import_partners('../data/partners.csv')  # import partner application data from partners.csv

    # import classroom information from classrooms.csv
    with open('../data/classrooms.csv') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.DictReader(classrooms_csv)
        group_num = 3
        for row in csv_reader:  # for each teacher application
            teacher_name = row['Name']
            teacher_phone = row['Cell Phone Number']
            school = row['School']
            email = row['Email Address']
            number_of_classes = row['Number of Classes']
            for i in range(int(number_of_classes)):  # for all of that teacher's classes
                group_num += 1
                class_num = i + 1  # class_num keeps track of which class out of the total being created
                # creates a Classroom object and adds it to global variable classroom_list
                classroom = Classroom(group_number=group_num,
                                      teacher_name=teacher_name,
                                      teacher_phone=teacher_phone,
                                      school=school,
                                      email=email,
                                      start_time=row[f'Start Time (Class {class_num} of {number_of_classes})'],
                                      end_time=row[f'End Time (Class {class_num} of {number_of_classes})'],
                                      day=row[f'Days (Class {class_num} of {number_of_classes})'].strip()
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
            empty_classrooms.append(classroom)
        elif classroom.volunteers_assigned < MAX_TEAM_SIZE:
            partially_filled_classrooms.append(classroom)

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
            empty_classrooms.append(classroom)
            for volunteer in volunteer_list:
                if volunteer.group_number == classroom.group_number:
                    volunteer.set_group_number(-1)

    for volunteer in volunteer_list:
        if volunteer.group_number == -1:
            unassigned_volunteers.append(volunteer)
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
        csv_writer.writerow(
            ['Group Number', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Team Leader', 'Teacher', 'Day',
             'Start Time', 'End Time']
        )
        for volunteer in volunteer_list:
            if volunteer.group_number == -1:
                unassigned_volunteers += 1
            else:
                group_size[volunteer.group_number] += 1
                assigned_class = classroom_list[volunteer.group_number - 4]
                start_time = str(assigned_class.start_time)
                end_time = str(assigned_class.end_time)
            csv_writer.writerow(
                [
                    volunteer.group_number,
                    volunteer.first,
                    volunteer.last,
                    volunteer.email,
                    volunteer.phone,
                    (lambda x: 'True' if x else '')(volunteer.assigned_t_leader),
                    assigned_class.teacher,
                    assigned_class.day_of_week,
                    (lambda x: x[0:2] + ':' + x[2:] if len(x) == 4 else x[0:1] + ":" + x[1:])(start_time),
                    (lambda x: x[0:2] + ':' + x[2:] if len(x) == 4 else x[0:1] + ":" + x[1:])(end_time)
                ]
            )

        with open('../results/classrooms.csv', 'w', newline='') as classrooms_csv:
            csv_writer = csv.writer(classrooms_csv, delimiter=',')
            csv_writer.writerow(
                ['Group Number', 'Teacher', 'Phone', 'School', 'School Phone', 'Email', 'Grade', 'Start Time',
                 'End Time', 'Day']
            )
            for classroom in classroom_list:
                csv_writer.writerow(
                    [
                        classroom.group_number,
                        classroom.teacher,
                        '',
                        classroom.school,
                        '',
                        classroom.teacher_email,
                        '',
                        classroom.start_time,
                        classroom.end_time,
                        classroom.day_of_week
                    ]
                )

    print('There were {} unassigned volunteers.'.format(unassigned_volunteers))

    # TODO: Remove after testing?
    for classroom in classroom_list:
        print("{} volunteers assigned to group {}".format(group_size[classroom.group_number], classroom.group_number))


# runs main
if __name__ == '__main__':
    main()
