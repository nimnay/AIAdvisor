import utils

from models import Student
from utils import callAPI

if __name__ == '__main__':
    print("Enter your name: ")
    name = input().strip()

    print("Enter courses you have **already completed**, separated by commas (e.g., CPSC 1010, ENGL 1030):")
    completed_courses = input().strip().split(', ') if input().strip() else []

    print("Enter courses you are **currently enrolled in**, separated by commas (or leave blank if none):")
    current_courses = input().strip().split(', ') if input().strip() else []

    print("Enter any time slot constraints (e.g., 3-4pm, or leave blank if none):")
    time_constraints = input().strip()

    # Create student object
    student = {
        "name": name,
        "completed_courses": completed_courses,
        "current_courses": current_courses,
        "time_constraints": time_constraints
    }

    response = callAPI(student)
    'response = callAPI()'