import csv

from scheduler import Scheduler


def main():

    vsvs_scheduler = Scheduler()
    partner_errors = vsvs_scheduler.create_assignments()
    print(partner_errors)

    with open('results/assignments.csv', 'w', newline='') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        csv_writer.writerow(
            ['Group Number', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Team Leader', 'Board Member',
             'Teacher', 'Day', 'Start Time', 'End Time']
        )

        group_num = 1
        for classroom in vsvs_scheduler.classrooms:
            if len(classroom.volunteers) >= 3:
                for volunteer in classroom.volunteers:
                    csv_writer.writerow(
                        [
                            group_num,
                            volunteer.first,
                            volunteer.last,
                            volunteer.email,
                            volunteer.phone,
                            (lambda x: 'True' if x else '')(volunteer.assigned_leader),
                            (lambda x: 'True' if x else '')(volunteer.board),
                            classroom.teacher.name,
                            classroom.weekday,
                            classroom.start_time.strftime('%I:%M %p'),
                            classroom.end_time.strftime('%I:%M %p')
                        ]
                    )
                group_num += 1

    with open('results/unassigned.csv', 'w', newline='') as unassigned_csv:
        csv_writer = csv.writer(unassigned_csv, delimiter=',')
        csv_writer.writerow(
            [ 'Group', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Team Leader', 'Board Member', 'Teacher',
             'Availability', 'Start', 'End', 'Day']
        )
        for classroom in vsvs_scheduler.classrooms:
            if len(classroom.volunteers) < 3:
                csv_writer.writerow(
                    [
                        '',
                        '',
                        classroom.teacher.name,
                        classroom.teacher.email,
                        classroom.teacher.phone,
                        '',
                        '',
                        'True',
                        '',
                        classroom.start_time.strftime('%I:%M %p'),
                        classroom.end_time.strftime('%I:%M %p'),
                        classroom.weekday
                    ]
                )
        csv_writer.writerow(['']*6)

        for volunteer in vsvs_scheduler.individuals:
            if volunteer.group_number == -1:
                csv_writer.writerow(
                    [
                        0,
                        volunteer.first,
                        volunteer.last,
                        volunteer.email,
                        volunteer.phone,
                        (lambda x: 'True' if x else '')(volunteer.assigned_leader),
                        (lambda x: 'True' if x else '')(volunteer.board),
                        '',
                        volunteer.availability
                    ]
                )


# runs main
if __name__ == '__main__':
    main()
