import utils

from models import Student
from utils import callAPI

if __name__ == '__main__':
    print("Enter your name: ")
    name = input()
    print("Enter your grade: ")
    grade = input()
    print("Enter any time constraints: ")
    time_constraints = input()
    student = Student(name, grade, time_constraints)

    response = callAPI(student)
    print(response)