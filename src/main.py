"""Main entry point for AI Advisor - Student Schedule Planner."""

import logging
import sys
from typing import Dict, List, Optional

from src.utils import call_api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_user_input() -> Dict[str, any]:
    """
    Collect student information from user input.

    Returns:
        Dictionary containing student name, completed courses, current courses,
        and optional time constraints
    """
    print("=" * 60)
    print("AI Advisor - Student Schedule Planner")
    print("=" * 60)
    print()

    # Get student name
    print("Enter your name: ")
    name = input().strip()

    # Get completed courses
    print(
        "\nEnter courses you have **already completed**, separated by commas "
        "(e.g., CPSC 1010, ENGL 1030):"
    )
    completed_input = input().strip()
    completed_courses = (
        [course.strip() for course in completed_input.split(",") if course.strip()]
        if completed_input
        else []
    )

    # Get current courses
    print(
        "\nEnter courses you are **currently enrolled in**, separated by commas "
        "(or leave blank if none):"
    )
    current_input = input().strip()
    current_courses = (
        [course.strip() for course in current_input.split(",") if course.strip()]
        if current_input
        else []
    )

    # Get time constraints (optional)
    print(
        "\nEnter any time slot constraints (e.g., 'No classes before 10am', "
        "or leave blank if none):"
    )
    time_constraints = input().strip() or None

    # Build student dictionary
    student = {
        "name": name,
        "completed_courses": completed_courses,
        "current_courses": current_courses,
        "time_constraints": time_constraints,
    }

    return student


def display_recommendations(
    student_name: str, recommendations: Optional[List[str]]
) -> None:
    """
    Display the schedule recommendations to the user.

    Args:
        student_name: Name of the student
        recommendations: List of recommended courses, or None if failed
    """
    print("\n" + "=" * 60)
    print(f"Schedule Recommendations for {student_name}")
    print("=" * 60)

    if not recommendations:
        print("\n⚠️  Unable to generate recommendations at this time.")
        print("Please check the logs for more details.")
        return

    print("\nRecommended Schedule:\n")
    for i, course in enumerate(recommendations, 1):
        print(f"{i}. {course}")

    print("\n" + "=" * 60)


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Collect student information
        student = get_user_input()

        # Log student info (excluding personal details in production)
        logger.info("Processing schedule request for student: %s", student["name"])
        logger.debug("Completed courses: %d", len(student["completed_courses"]))
        logger.debug("Current courses: %d", len(student["current_courses"]))

        # Call API to get recommendations
        print("\n🔄 Generating schedule recommendations...")
        print("This may take a moment...\n")

        recommendations = call_api(student)

        # Display results
        display_recommendations(student["name"], recommendations)

        return 0 if recommendations else 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        return 1
    except Exception as e:
        logger.exception("Unexpected error in main: %s", e)
        print("\n❌ An unexpected error occurred. Please check the logs.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
