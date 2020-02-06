import csv
import src.person
import src.partners

# make a way to detect if name submitted for partner application is in database or not (current application already does this)

TEAM_MAX_MEMBERS = 4
TEAM_MIN_MEMBERS = 3

def main():

    volunteer_list = [] # list of all the volunteers that will be iterated through; STARTS AT INDEX 1 TO MATCH APPLICATION ID

    volunteer_list.append("SKIP THIS LINE") # ignore index 0 bc we want index to match application id #, which starts at 1


    # imports individual application data
    with open('../test/volunteers.csv') as volunteer_csv:  # opens volunteers.csv as volunteers_csv
        csv_reader = csv.reader(volunteer_csv, delimiter=',')  # csv_reader will divide volunteers_csv by commas
        for row in csv_reader:
            volunteer_list.append(src.person.Person(row[1], row[2], row[3], row[4], row[8], row[9], row[10], row[12], row[13], row[15], row[16], row[18], row[20]))  # creates Person objects and adds them to volunteer_list, indices correspond to columns of responses in volunteers.csv

    # imports partner application data
    with open('../test/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # csv_reader will divide partners_csv by commas
        for row in csv_reader:
            volunteer_list[row[1]].addPartners(row[2], row[3], row[4], row[6])  # calling addPartner method on line of volunteer that signed partners up (volunteer_list[row[1]])


    # import classroom information once we get to see example sheet

    for volunteer in volunteer_list:
        if ((volunteer.groupNumber == 0) && (volunteer.partner_app)):
            assignTeam(volunteer) # will have to go into partners object and add all partners to same team

    for volunteer in volunteer_list:
        if ((volunteer.groupNumber == 0) and (volunteer.car > TEAM_MIN_MEMBERS)): # figure this out: keep their group under car capacity or dont allow car unless it is TEAM_MAX_MEMBERS
            assignTeam(volunteer)

    for volunteer in volunteer_list:
        if ((volunteer.groupNumber == 0) && (volunteer.t_leader)):
            assignTeam(volunteer)


# runs main
if __name__ == "__main__":
    main()
