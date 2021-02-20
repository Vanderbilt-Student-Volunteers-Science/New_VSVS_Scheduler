# New_VSVS_Scheduler

**This project is not complete. If you have improvements, please open a pull request.**

![Python application](https://github.com/VanderbiltSVS/New_VSVS_Scheduler/workflows/Python%20application/badge.svg?branch=develop)

Project started October 2019

**Authors**: 2020 VSVS IT Committee (David Ward, Michael Selzer, Katie Helman, Nilai Vemula, Rishi Das)

**Description**: Imports data from data/classrooms.csv, data/individuals.csv, and data/partners.csv and assigns
 volunteers to groups. Assigns partners, then drivers, then team leaders, then everyone else. Outputs results in results/assignments.csv.

<hr>

## Getting Started

In order to run this program, you will first need to prepare three input files. Currently, these three input files
 come from the Google Forms we are using as the applications. Click on the following file names to get specifics
  about the specifications of each input file.
1. [`data/classrooms.csv`](docs/classrooms.md)
2. [`data/individuals.csv`](docs/individuals.md)
3. [`data/partners.csv`](docs/partners.md)

<details><summary>Detailed Instructions on Generating Input Files</summary>
<p>

Before running:
  1. Export the responses to the individual application to csv and call it individuals.csv
  2. Export the responses to the partner application to csv and call it partners.csv
  3. Copy and paste (don't export) the classroom table from Access with headings and call it classrooms.csv (or manually collate responses from teacher sign up form)
  4. Place individuals.csv, partners.csv, and classrooms.csv into the data directory of this program

</p>
</details>

Assuming there are no deviations from the format outlined above, the program can be run through the main method in
 `src/main.py`. Assuming successful operations, there will be one output file generated: `results/assignments.csv
 `. If the `results/` directory does not exist, the program will create it for you.
 
**Note:** If you make any changes, be sure to add unit tests for any new code. Read [this documentation](docs/automated_testing.md) for more information. Tests are run on each
commit through GitHub Actions. The badge at the top of this README tells us if tests are passing or failing.
 
## Repository Structure

This repository has/will have the following files:
```
- data/ (input csv files)
    - classrooms.csv
    - individuals.csv
    - partners.csv
- docs/
    - (various markdown files for more specific documentation)
- results/ (outputs generated from program)
    - assignments.csv
- src/
    - assign.py (functions for assigning volunteers, partners, drivers, etc)
    - classroom.py (contains the Classroom class)
    - convertSchedule.py (functions for creating schedule arrays and converting to military time)
    - globalAttributes.py (list of constants)
    - main.py (sorting algorithm, handle input + output files)
    - volunteer.py (contains the Volunteer class) 
```
 
 
## Sorting Algorithm

Description of how the sorting algo works, flowchart, etc

### Classroom Class

The classroom class has the following members:

- group_number
- teacher_name
- teacher_phone
- school
- teacher_email
- day_of_week
- volunteers_assigned
- t_leader (does this classroom have a team leader?)
- driver (does this classroom have a driver?)
- class_start_time (time the class starts in military time)
- class_end_time (time the class ends in military time)
- free_time_start (the latest time a volunteer can start being available and be able to make this lesson)
- volunteer_time_needed (minutes of free time needed starting at free_time_start for a volunteer to be able to make
 this lesson)
- start_time_schedule_index (the index in the array of Volunteer attribute free_time_array (or partner_schedule) that needs to be >= volunteer_time_needed for a volunteer to be able to visit this classroom)
- has_in_person_volunteer (does this classroom have at least one in-person volunteer?)

### Volunteer Class

The volunteer class has the following members:

- applied_t_leader (volunteer applied to be a team leader?)
- car_passengers (people a driver can drive (not including driver))
- driver (if they have a car that can carry the MAX_TEAM_SIZE)
- schedule_array (boolean array containing an index for each 15-min block between the times of 7:15am-3:45pm, Monday through Thursday)
- free_time_array (boolean array for same time slots as above, showing if volunteer is free)
- group_number (-1 if unassigned)
- partners (number of other partners)
- partner_indexes
- partner_free_time_array
- assigned_driver (Was the volunteer assigned to be the driver for their group?)
- assigned_t_leader (Was the volunteer assigned to be their group's team leader?)
- classrooms_possible = (Number of classrooms the volunteer can make according to their schedule.)
- is_in_person (True if the volunteer is in person, False if they are remote.)

## To-do

**Look in Issues and/or Projects**

### Testing Metrics:
- [ ] people can make classrooms they're assigned to
- [ ] groups are assigned together
- [ ] each group has at least one in-person
- [ ] see how many groups of <MAX there are

## Spring 2021 Changes
- 5 volunteers per group
- Board priority for team assignment + team leader
- Better parsing of partner app (strip methods)
