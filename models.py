

class Student:
    """
    Represents a Student with a name, grade, and time constraints.

    :param name: The student's name
    :param grade: The student's current grade
    :param time_constraints: Time the student does not want class
    """

    def __init__(self, name: str,  classes_taken: str, time_constraints: str):
        self.name = name
        # Convert the input string into a list of classes
        self.classes_taken = classes_taken.split(", ")  # Assumes input is comma-separated
        self.time_constraints = time_constraints

    def get_classes_taken(self):
        return self.classes_taken

    def get_time_constraints(self):
        return self.time_constraints

    def __str__(self):
        return f"Student: {self.name}, Grade: {self.classes_taken}, Time Constraints: {self.time_constraints}"
