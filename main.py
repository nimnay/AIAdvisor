import utils

from models import Student
from utils import callAPI

if __name__ == '__main__':
    print("Enter your name: ")
    name = input()
    print("Enter classes already taken with a space in between each: e.g CPSC 1010, ENG 1030")
    classes = input()
    print("Enter any time slot constraints: e.g. 3-4pm")
    time_constraints = input()
    student = Student(name, classes, time_constraints)

    response = callAPI()