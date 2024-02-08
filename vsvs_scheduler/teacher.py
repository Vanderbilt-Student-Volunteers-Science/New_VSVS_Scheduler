
class Teacher:

    def __init__(self, name: str, phone: str, school: str, email: str, weekday_preferences: list) -> None:
        """ Teacher object that holds information about a teacher."""
        
        self.name = name
        self.phone = phone #USE REGEX
        self.school = school
        self.email = email #USE REGEX
        self.weekdays = weekday_preferences
        self.weekday_idx = 0
        self.weekday = self.weekdays[self.weekday_idx]
        self.classrooms = []
    
    def next_weekday(self) -> None:
        """ Updates the weekday to the next weekday preference. """
        possible_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        if self.weekday_idx < 3 and self.weekdays[self.weekday_idx + 1] in possible_weekdays:
            self.weekday_idx += 1
            self.weekday = self.weekdays[self.weekday_idx]
    
    def add_classrooms(self, classroom) -> None:
        """ Adds classrooms to the teacher's list of classrooms. """
        self.classrooms.append(classroom)
    
    def unassign_volunteers(self) -> None:
        """ Unassigns volunteers from the classroom and resets their group number and assigned_leader status."""
        for classroom in self.classrooms:
            classroom.unassign_volunteers()
    
    def reset_weekday(self) -> None:
        """ Resets the weekday to the first weekday preference. """
        self.weekday_idx = 0
        self.weekday = self.weekdays[self.weekday_idx]


