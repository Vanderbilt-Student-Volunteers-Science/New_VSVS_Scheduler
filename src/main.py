import csv
import src.volunteer
import src.partners
import src.classroom
import src.militaryTime

# make a way to detect if name submitted for partner application is in database or not (current application already does this)

TEAM_MAX_MEMBERS = 4
TEAM_MIN_MEMBERS = 3

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
            classroom_list.append(src.classroom.Classroom(row[3], row[4], row[6], row[9], src.militaryTime.convert_to_military(row[11]), src.militaryTime.convert_to_military(row[12]), row[13]))  # creates Classroom object

    # set preassigned volunteers in classroom data before assigning
    for volunteer in volunteer_list:
        if volunteer.group_number != 0:
            classroom_list[volunteer.group_number].add_preassigned_volunteer()


    # ASSIGN VOLUNTEERS

    for volunteer in volunteer_list:
        if volunteer.group_number == 0 and volunteer.partner_app:
            assign_team(volunteer) # will have to go into partners object and add all partners to same team

    for volunteer in volunteer_list:
        if volunteer.group_number == 0 and volunteer.car_passengers > TEAM_MIN_MEMBERS: # figure this out: keep their group under car capacity or dont allow car unless it is TEAM_MAX_MEMBERS
            assign_team(volunteer)

    for volunteer in volunteer_list:
        if volunteer.group_number == 0 and volunteer.t_leader:
            assign_team(volunteer)


# runs main
if __name__ == "__main__":
    main()
