import utils

from models import Student
from utils import callAPI

if __name__ == '__main__':
    print("Enter your name: ")
    name = input()
    print("Enter classes already taken with a space in between each: ")
    classes = input()
    print("Enter any time constraints: ")
    time_constraints = input()
    student = Student(name, grade, time_constraints)

    response = callAPI()