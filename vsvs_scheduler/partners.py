from volunteer import Volunteer
from classroom import Classroom


class Partners:
    def __init__(self, group: list[Volunteer]):
        self.members = group
        self.possible_classrooms = 0
        self.group_number = -1

    def can_make_class(self, classroom: Classroom, max_team_size: int):
        for member in self.members:
            if not member.can_make_class(classroom):
                return False
        return max_team_size - len(classroom.volunteers) >= len(self.members)

    def increment_possible_classrooms(self):
        self.possible_classrooms += 1
        for member in self.members:
            member.possible_classrooms += 1

    def assign_partners(self, classroom: Classroom):
        for member in self.members:
            classroom.assign_volunteer(member)
        self.group_number = classroom.group_number

    def __str__(self):
        result = ""
        for member in self.members:
            result += member.__str__
        return result