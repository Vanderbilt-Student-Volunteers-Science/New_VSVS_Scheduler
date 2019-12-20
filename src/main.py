import csv
import src.person


# Before running, name csv file exported from volunteer signup form "volunteers.csv" and place in test directory.
# https://docs.google.com/forms/d/1Rf12tr3IqDWAjw2a-gq_7APjnBESUoeyzkN-H0sdPZs/edit

def main():

    volunteer_list = [] # list of all the volunteers

    with open('../test/volunteers.csv') as volunteer_csv:  # opens volunteers.csv as volunteers_csv
        csv_reader = csv.reader(volunteer_csv, delimiter=',')  # csv_reader will divide volunteers_csv by commas
        line = 0
        for row in csv_reader:
            if line > 0:  # top row is column headers
                volunteer_list.append(src.person.Person(row[1], row[2], row[8], row[9], row[12], row[15]))  # creates Person objects and adds them to volunteer_list, indices correspond to columns of responses in volunteers.csv
            line += 1


# runs main
if __name__ == "__main__":
    main()
