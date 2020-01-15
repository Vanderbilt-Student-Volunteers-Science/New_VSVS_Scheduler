import csv
import src.person
import src.partners

# make a way to detect if name submitted for partner application is in database or not (current application already does this)

# Before running, name csv file exported from individual signup form "volunteers.csv" and csv exported from partner signup "partners.csv" and place in test directory.
# volunteers: https://docs.google.com/forms/d/1Rf12tr3IqDWAjw2a-gq_7APjnBESUoeyzkN-H0sdPZs/edit

TEAM_MAX_MEMBERS = 4
TEAM_MIN_MEMBERS = 3

def main():

    volunteer_list = [] # list of all the volunteers that will be iterated through

    with open('../test/volunteers.csv') as volunteer_csv:  # opens volunteers.csv as volunteers_csv
        csv_reader = csv.reader(volunteer_csv, delimiter=',')  # csv_reader will divide volunteers_csv by commas
        line = 0
        for row in csv_reader:
            if line > 0:  # top row is column headers
                volunteer_list.append(src.person.Person(row[1], row[2], row[8], row[9], row[12], row[15]))  # creates Person objects and adds them to volunteer_list, indices correspond to columns of responses in volunteers.csv
            line += 1

    with open('../test/partners.csv') as partners_csv:  # opens partners.csv as partners_csv
        csv_reader = csv.reader(partners_csv, delimiter=',')  # csv_reader will divide partners_csv by commas
        line = 0
        for row in csv_reader:
            if line > 0:  # top row is column headers
                volunteer_list[row[1]].addPartners(row[2], row[3], row[4])  # calling addPartner method on line of volunteer that signed partners up (volunteer_list[row[1]])
            line += 1


    # import classroom information once we get to see example sheet

    for volunteer in volunteer_list:
        if (volunteer.partner_app):
            assignTeam(volunteer) # will have to go into partners object and add all partners to same team

    for volunteer in volunteer_list:
        if (not(volunteer.onTeam) and volunteer.car > TEAM_MIN_MEMBERS): # figure this out: keep their group under car capacity or dont allow car unless it is TEAM_MAX_MEMBERS
            assignTeam(volunteer)

    for volunteer in volunteer_list:
        if (volunteer.t_leader):
            assignTeam(volunteer)


# runs main
if __name__ == "__main__":
    main()
