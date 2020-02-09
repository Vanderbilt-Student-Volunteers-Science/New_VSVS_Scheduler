import csv
import src.volunteer
import src.partners
import src.classroom

# TODO: make sure input school names are uniform ex: Head Magnet/Head Middle Magnet/Head won't work

MAX_TEAM_SIZE = 4
MIN_TEAM_SIZE = 3
# SCHOOL TRAVEL TIME CONSTANTS IN classroom.py

def main():

    volunteer_list = [] # list of all the volunteers that will be iterated through; STARTS AT INDEX 1 TO MATCH APPLICATION ID
    classroom_list = [] # list of all the classroom times to to assign groups to

    volunteer_list.append("SKIP THIS LINE") # ignore index 0 bc we want index to match application id #, which starts at 1 (bc weird SQL int)
    classroom_list.append("SKIP THIS LINE") # ignore index 0 bc we want index to match group number, which starts at 1 (groupNumber initialized at 0)


    #  IMPORT FILE DATA

    # import individual application data
    with open('../test/individuals.csv') as individuals_csv:  # opens individuals.csv as individuals_csv
        csv_reader = csv.reader(individuals_csv, delimiter=',')  # csv_reader will divide individuals_csv by commas
        for row in csv_reader:
            volunteer_list.append(src.volunteer.Volunteer(row[1], row[2], row[3], row[4], row[8], row[9], row[10], row[12], row[13], row[16], row[18], row[20]))  # creates Volunteer objects and adds them to volunteer_list, indices correspond to columns of responses in volunteers.csv

    # import partner application data
    with open('../test/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # csv_reader will divide partners_csv by commas
        for row in csv_reader:
            volunteer_list[row[1]].add_partners(row[2], row[3], row[4], row[6])  # calling addPartner method on line of volunteer that signed partners up (volunteer_list[row[1]])

    # import classroom information
    with open('../test/classrooms.csv') as classrooms_csv:  # opens classrooms.csv as classrooms_csv
        csv_reader = csv.reader(classrooms_csv, delimiter=',')  # csv_reader will divide classrooms_csv by commas
        for row in csv_reader:
            classroom_list.append(src.classroom.Classroom(row[3], row[4], row[6], row[9], row[11], row[12], row[13]))  # creates Classroom object

    # set preassigned volunteers in classroom data before assigning
    for volunteer in volunteer_list:
        if volunteer.group_number != 0:
            classroom_list[volunteer.group_number].add_volunteer()


    # ASSIGN VOLUNTEERS

    for volunteer in volunteer_list:
        if volunteer.group_number == 0 and volunteer.partner_app:
            assign_partners(volunteer) # will have to go into partners object and add all partners to same team

    for volunteer in volunteer_list:
        if volunteer.group_number == 0 and volunteer.car_passengers > MIN_TEAM_SIZE: # figure this out: keep their group under car capacity or don't allow car unless it is TEAM_MAX_MEMBERS
            assign_team(volunteer)

    for volunteer in volunteer_list:
        if volunteer.group_number == 0 and volunteer.t_leader:
            assign_team(volunteer)


    # OUTPUT RESULTS

    with open('../results/assignments.csv') as assignments_csv:
        csv_writer = csv.writer(assignments_csv, delimiter=',')
        for volunteer_id in range(1, len(volunteer_list)):
            csv_writer.writerow([volunteer_id, volunteer_list[volunteer_id].group_number, volunteer_list[volunteer_id].first, volunteer_list[volunteer_id].last, volunteer_list[volunteer_id].email, volunteer_list[volunteer_id].phone])




# runs main
if __name__ == "__main__":
    main()
