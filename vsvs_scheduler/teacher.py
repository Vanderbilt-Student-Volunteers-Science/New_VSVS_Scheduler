
class Teacher:
    """
    The Teacher class represents a teacher. 
    It holds information about the teacher, their weekday preferences, and the classrooms they have.
    """
    def __init__(self, name: str, phone: str, school: str, email: str, weekday_preferences: list) -> None:
        """
        Initializes a Teacher object with the given name, phone number, school, email, and weekday preferences.

        Parameters:
        name   (str): The name of the teacher.
        phone  (str): The phone number of the teacher.
        school (str): The school where the teacher works.
        email  (str): The email address of the teacher.
        weekday_preferences (list): The teacher's weekday preferences for classes.
        """
        
        self.name = name
        self.phone = phone # TODO: Validate with regex
        self.school = school
        self.email = email # TODO: Validate with regex
        self.weekdays = weekday_preferences
        self.weekday_idx = 0 # Index to keep track of the current weekday preference
        self.weekday = self.weekdays[self.weekday_idx] # The current weekday preference
        self.classrooms = []  # List to hold the classrooms the teacher has
    
    def next_weekday(self) -> None:
        """ 
        Updates the weekday to the next weekday preference. 
        """
        possible_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]

        # Check if there is a next weekday preference and if it is a valid weekday
        if self.weekday_idx < 3 and self.weekdays[self.weekday_idx + 1] in possible_weekdays:
            self.weekday_idx += 1
            self.weekday = self.weekdays[self.weekday_idx]
    
    def add_classrooms(self, classroom) -> None:
        """
        Adds a classroom to the teacher's list of classrooms.

        Parameters:
        classroom (Classroom): The classroom to be added.
        """
        self.classrooms.append(classroom)
    
    def unassign_volunteers(self) -> None:
        """ 
        Unassigns volunteers from the classroom and resets their group number and assigned_leader status.
        """
        for classroom in self.classrooms:
            classroom.unassign_volunteers()
    
    def reset_weekday(self) -> None:
        """ 
        Resets the weekday to the first weekday preference. 
        """
        self.weekday_idx = 0
        self.weekday = self.weekdays[self.weekday_idx]


