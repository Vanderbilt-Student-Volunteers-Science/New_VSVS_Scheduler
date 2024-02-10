from volunteer import Volunteer
from classroom import Classroom


class Partners:
    def __init__(self, group: list[Volunteer]):
        """ Partners object that holds information about a group of partners."""

        self.members = group
        self.possible_classrooms = 0
        self.group_number = -1



    def can_make_class(self, classroom: Classroom, max_team_size: int):
        """ Returns True if the group can make the class, False otherwise."""

        for member in self.members:
            if not member.can_make_class(classroom):
                return False
            
        # if the group can make the class, check if there is enough space for the group
        return max_team_size - len(classroom.volunteers) >= len(self.members)



    def increment_possible_classrooms(self):
        """ Increments the number of possible classrooms the group can make."""

        self.possible_classrooms += 1
        for member in self.members:
            member.possible_classrooms += 1



    def assign_partners(self, classroom: Classroom):
        """ Assigns the group to the classroom."""

        for member in self.members:
            classroom.assign_volunteer(member)
        self.group_number = classroom.group_number



    def __repr__(self):
        return str(self.members)