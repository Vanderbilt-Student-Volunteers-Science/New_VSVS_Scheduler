import csv, os, logging
from scheduler import Scheduler
from globals import ASSIGNMENTS_DIRECTORY, MIN_TEAM_SIZE


def main():
    logging.basicConfig(filename='vsvs_scheduler.log', filemode='w', format='%(levelname)s - %(message)s', level=logging.DEBUG)

    vsvs_scheduler = Scheduler()
    partner_errors = vsvs_scheduler.create_assignments()
    print(partner_errors)

    if not os.path.isdir(ASSIGNMENTS_DIRECTORY):
        os.mkdir(ASSIGNMENTS_DIRECTORY)
    
    results_file_path = os.path.join(ASSIGNMENTS_DIRECTORY, 'assignments.csv')

    with open(results_file_path, 'w', newline='') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        csv_writer.writerow(
            ['Group Number', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Team Leader', 'Board Member',
             'Teacher', 'Day', 'Start Time', 'End Time']
        )

        group_num = 1
        for classroom in vsvs_scheduler.classrooms:
            if len(classroom.volunteers) >= MIN_TEAM_SIZE:
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

    unassigned_file_path = os.path.join(ASSIGNMENTS_DIRECTORY, 'unassigned.csv')
    with open(unassigned_file_path, 'w', newline='') as unassigned_csv:
        csv_writer = csv.writer(unassigned_csv, delimiter=',')
        csv_writer.writerow(
            [ 'Group', 'First Name', 'Last Name', 'Email', 'Phone Number', 'Team Leader', 'Board Member', 'Teacher',
             'Availability', 'Start', 'End', 'Day']
        )
        for classroom in vsvs_scheduler.classrooms:
            if len(classroom.volunteers) < MIN_TEAM_SIZE:
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
                        classroom.teacher.weekday
                    ]
                )
        csv_writer.writerow(['']*6)

        for volunteer in vsvs_scheduler.volunteers:
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
                    ]
                )


# runs main
if __name__ == '__main__':
    main()
