

class Student:
    """
    Represents a Student with a name, grade, and time constraints.

    :param name: The student's name
    :param grade: The student's current grade
    :param time_constraints: Time the student does not want class
    """

    def __init__(self, name: str, grade: str, time_constraints: str):
        self.name = name
        self.grade = grade
        self.time_constraints = time_constraints

    def get_grade(self):
        return self.grade

    def get_time_constraints(self):
        return self.time_constraints

    def __str__(self):
        return f"Student: {self.name}, Grade: {self.grade}, Time Constraints: {self.time_constraints}"
