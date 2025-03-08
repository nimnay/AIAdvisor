import utils


from utils import callAPI
if __name__ == '__main__':
    print("Enter your name: ")
    name = input().strip()

    print("Enter courses you have **already completed**, separated by commas (e.g., CPSC 1010, ENGL 1030):")
    completed_input = input().strip()
    completed_courses = [course.strip() for course in completed_input.split(',') if course.strip()] if completed_input else []

    print("Enter courses you are **currently enrolled in**, separated by commas (or leave blank if none):")
    current_input = input().strip()
    current_courses = [course.strip() for course in current_input.split(',') if course.strip()] if current_input else []

    "print(Enter any time slot constraints (e.g., 3-4pm, or leave blank if none):)"
    "time_constraints = input().strip() or None "

    # Create student dictionary
    student = {
        "name": name,
        "completed_courses": completed_courses,
        "current_courses": current_courses,
    }



    response = callAPI(student)
    print("\nResponse from API:\n", response)