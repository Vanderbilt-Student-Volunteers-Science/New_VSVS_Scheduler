import warnings, logging
from classroom import Classroom
from volunteer import Volunteer
from partners import Partners
from data_uploader import DataUploader
from globals import MAX_TEAM_SIZE, MIN_TEAM_SIZE



class Scheduler:
    def __init__(self):
        """
        Scheduler object that holds information about the schedule and the volunteers and classrooms.
        """
        logging.info('Initializing Scheduler')

        # Initialize data uploader and import data
        data = DataUploader()
        data.import_data()

        # Assign volunteers, classrooms, and partners from the imported data
        self.volunteers: list[Volunteer] = data.volunteers
        self.classrooms: list[Classroom] = data.classrooms
        self.partners:   list[Partners] = data.partners

        # Initialize list for incomplete classrooms
        self.incomplete_classrooms = self.classrooms.copy()



    def create_assignments(self):
        """
        Creates assignments for partners and volunteers to classrooms.
        """

        logging.info('Creating assignments')

        # Assign partners to classrooms
        self.assign_partners()

        # Assign volunteers to classrooms based on their roles
        self.assign_volunteers("board")
        self.assign_volunteers("leaders")
        self.assign_volunteers()

        num_days_to_try = 4

        while num_days_to_try > 0 and self.incomplete_classrooms:

            logging.info(f'Day preference: {5 - num_days_to_try}')

            updated_teachers = []
            for classroom in self.incomplete_classrooms:
                # Unassign volunteers from the classroom
                classroom.unassign_volunteers()
                # Change to the next preferred day if the teacher hasn't been updated yet
                if classroom.teacher not in updated_teachers:
                    classroom.change_to_next_preferred_day()
                    updated_teachers.append(classroom.teacher)
            # Assign volunteers to classrooms
            self.assign_volunteers()
            num_days_to_try -= 1
        
        logging.info('Second to last round of assignments -- assigning volunteers to classrooms without leaders') 
        # Reset the weekday for teachers of incomplete classrooms
        num_days_to_try = 4
        updated_teachers = []
        for classroom in self.incomplete_classrooms:
            if classroom.teacher not in updated_teachers:
                classroom.teacher.reset_weekday()
                updated_teachers.append(classroom.teacher)

        while num_days_to_try > 0 and self.incomplete_classrooms:
            updated_teachers = []
            for classroom in self.incomplete_classrooms:
                classroom.unassign_volunteers()
                if classroom.teacher not in updated_teachers:
                    classroom.change_to_next_preferred_day()
                    updated_teachers.append(classroom.teacher)

            # Assign volunteers to classrooms in the second to last round
            self.assign_volunteers("second_to_last_round")
            num_days_to_try -= 1
        
        logging.info('Last round of assignments -- assigning volunteers to classrooms even if min team size is reached')
         # Assign volunteers in the last round and freeze the weekday for all classrooms
        self.assign_volunteers("last_round")
        for classroom in self.classrooms:
            classroom.freeze_weekday()

        # Check for missing team leaders or classrooms without the necessary number of volunteers
        missing_team_leaders = [classroom for classroom in self.classrooms if not classroom.team_leader and len(classroom.volunteers) >= MIN_TEAM_SIZE]
        if missing_team_leaders:
            logging.warning(f'WARNING: Classrooms are missing team leaders: {missing_team_leaders}\n')
        if self.incomplete_classrooms:
            logging.warning(f'WARNING: Classrooms without necessary number of volunteers {self.incomplete_classrooms}\n')
    
    def assign_partners(self):
        """
        Assigns partners to classrooms and returns a list of unassigned partners.
        """
        logging.info('Assigning partners')
        
        # Find possible matches between classrooms and partners
        self.find_possible_classroom_and_partners_matches()
        idx = 0
        unassigned_groups = []

        for group in self.partners:
            # Try to assign the group to a classroom
            while group.group_number == -1 and idx < len(self.incomplete_classrooms):
                curr_class = self.incomplete_classrooms[idx]
                if group.can_make_class(curr_class, MAX_TEAM_SIZE):
                    group.assign_partners(curr_class)

                    # Remove the classroom from the list of incomplete classrooms if it has reached the min team size
                    if len(curr_class.volunteers) >= MIN_TEAM_SIZE:
                        self.incomplete_classrooms.remove(curr_class)
                else:
                    idx += 1
            
            # Add the group to the list of unassigned groups if it couldn't be assigned
            if group.group_number == -1:
                unassigned_groups.append(group)
        
        logging.info(f'Unassigned partners: {unassigned_groups}')
    


    def assign_volunteers(self, volunteer_type: str = "default"):
        """
        Assigns volunteers to classrooms based on the volunteer_type parameter.
        The volunteer_type parameter can be "default", "leaders", "board", "last_round", or "second_to_last_round".
        """
        logging.info(f'Assigning volunteers of type: {volunteer_type}')
        # Find possible matches between classrooms and volunteers
        self.find_possible_classroom_and_volunteer_matches()

        # By default, consider all volunteers
        volunteer_list = self.volunteers

        # If volunteer_type is "leaders", consider only volunteers who are leaders
        if volunteer_type == "leaders":
            volunteer_list = [volunteer for volunteer in self.volunteers if volunteer.leader_app]

        # If volunteer_type is "board", consider only volunteers who are on the board
        elif volunteer_type == "board":
            volunteer_list = [volunteer for volunteer in self.volunteers if volunteer.board]
        
        # For "last_round", we consider all classrooms, not just the incomplete ones
        if volunteer_type == "last_round":
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.classrooms):
                    classroom = self.classrooms[idx]
                    if volunteer.can_make_class_last_round(classroom) and (len(classroom.volunteers) < MAX_TEAM_SIZE):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)
                    else:
                        idx += 1
        
        # For "second_to_last_round", we freeze the weekday for classrooms that reach the minimum team size
        elif volunteer_type == "second_to_last_round":
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                    classroom = self.incomplete_classrooms[idx]
                    if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)
                        if len(classroom.volunteers) >= MIN_TEAM_SIZE:
                            self.incomplete_classrooms.remove(classroom)
                            classroom.freeze_weekday()
                    else:
                        idx += 1

        else:
            # For "default", we unassign volunteers for incomplete classes at the end
            for volunteer in volunteer_list:
                idx = 0
                while volunteer.group_number == -1 and idx < len(self.incomplete_classrooms):
                    classroom = self.incomplete_classrooms[idx]
                    if volunteer.can_make_class(classroom) and (volunteer_type == "default" or not classroom.team_leader):
                        classroom.assign_volunteer(volunteer)
                        volunteer.assign_classroom(classroom)

                        # We remove classrooms from the list of incomplete classrooms once they reach the minimum team size
                        if len(classroom.volunteers) >= MIN_TEAM_SIZE:
                            self.incomplete_classrooms.remove(classroom)
                    else:
                        idx += 1
            self.unassign_volunteers_for_incomplete_classes()

        self.incomplete_classrooms.sort(key=lambda classroom: len(classroom.volunteers), reverse=True)

    
    def unassign_volunteers_for_incomplete_classes(self):
        """
        Unassigns volunteers for classrooms that are still incomplete.
        Also adds back any classrooms of the teacher of the current classroom that are not already in the list of incomplete classrooms.
        """
        logging.info('Unassigning volunteers for incomplete classes')

        for classroom in self.incomplete_classrooms:
            classroom.teacher.unassign_volunteers()

            # Add the classroom back to the incomplete_classrooms list if it is not already there
            self.incomplete_classrooms += [room for room in classroom.teacher.classrooms if room not in self.incomplete_classrooms]


    def find_possible_classroom_and_partners_matches(self):
        """
        Finds the number of possible classrooms each partner group can make and the number of possible partner groups each classroom can have.
        Sorts the partners and classrooms based on the number of possible matches.
        """

        for group in self.partners:
            for classroom in self.incomplete_classrooms:
                if group.can_make_class(classroom, MAX_TEAM_SIZE):
                    group.increment_possible_classrooms()
                    classroom.possible_partner_groups += 1
        self.partners.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_partner_groups)


        
    def find_possible_classroom_and_volunteer_matches(self):
        """
        Finds the number of possible classrooms each volunteer can make and the number of possible volunteers each classroom can have.
        Sorts the volunteers and classrooms based on the number of possible matches.
        """

        # find how many classrooms each volunteer can make
        for volunteer in self.volunteers:
            volunteer.possible_classrooms = sum(1 for classroom in self.incomplete_classrooms if volunteer.can_make_class(classroom))
        
        # find how many volunteers can make each classroom
        for classroom in self.incomplete_classrooms:
            classroom.possible_volunteers = sum(1 for volunteer in self.volunteers if volunteer.can_make_class(classroom)) 
            
        self.volunteers.sort(key=lambda person: person.possible_classrooms)
        self.incomplete_classrooms.sort(key=lambda clsroom: clsroom.possible_volunteers)

        

