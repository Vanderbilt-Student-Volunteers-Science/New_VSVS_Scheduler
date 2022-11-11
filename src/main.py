import csv
import os
from src.scheduler import Scheduler


def main():
    vsvs_scheduler = Scheduler(volunteer_file='../data/individuals.csv', classroom_file='../data/classrooms.csv',
                               partner_file='../data/partners.csv')


    # make list of unassigned volunteers, sort them by the number of classrooms they can make (fewest to greatest
    # number of classrooms they can make), then assign them to classroom groups (prioritizing adding them to
    # partially-filled classrooms over empty classrooms)


    # reassign volunteers that were assigned to groups of 1
    # TODO: think through this part better
    # unassigned_volunteers = []
    # for classroom in classroom_list:
    #     if classroom.volunteers_assigned == 1:
    #         empty_classrooms.append(classroom)
    #         for volunteer in volunteer_list:
    #             if volunteer.group_number == classroom.group_number:
    #                 volunteer.set_group_number(-1)
    #
    # for volunteer in volunteer_list:
    #     if volunteer.group_number == -1:
    #         unassigned_volunteers.append(volunteer)
    # assign_others(sort_by_availability(unassigned_volunteers))

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
        for volunteer in vsvs_scheduler.volunteer_list:
            if volunteer.group_number == -1:
                unassigned_volunteers += 1
            else:
                group_size[volunteer.group_number] += 1
                assigned_class = vsvs_scheduler.classroom_list[volunteer.group_number - 4]
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
            for classroom in vsvs_scheduler.classroom_list:
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
    for classroom in vsvs_scheduler.classroom_list:
        print("{} volunteers assigned to group {}".format(group_size[classroom.group_number], classroom.group_number))


# runs main
if __name__ == '__main__':
    main()
