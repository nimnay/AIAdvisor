"""Generate class schedules with randomized time slots."""

import json
import logging
import random
from pathlib import Path
from typing import Any, Dict, List

from src.config import MWF_TIME_SLOTS, TTH_TIME_SLOTS

# Configure logging
logger = logging.getLogger(__name__)


def generate_schedule_with_times(
    course_data: Dict[str, Any],
    num_sections: int = 3,
) -> List[Dict[str, Any]]:
    """
    Generate class schedules with randomized time slots.

    Args:
        course_data: Dictionary containing course information
        num_sections: Number of sections to generate per course

    Returns:
        List of courses with section information
    """
    schedule = []

    for category, details in course_data.items():
        if "class_options" in details:
            # Process general education classes
            for subcategory, courses in details["class_options"].items():
                for course in courses:
                    if "courses" in course:
                        # Nested courses (e.g., labs with lectures)
                        for sub_course in course["courses"]:
                            schedule.append(
                                _add_course_with_sections(
                                    sub_course, num_sections
                                )
                            )
                    else:
                        schedule.append(
                            _add_course_with_sections(course, num_sections)
                        )

        elif "major_related_classes" in details:
            # Process major-specific classes
            for year, courses in details["major_related_classes"].items():
                for course in courses:
                    if "paths" in course:
                        # Handle course paths
                        for path in course["paths"]:
                            for sub_course in path["courses"]:
                                schedule.append(
                                    _add_course_with_sections(
                                        sub_course, num_sections
                                    )
                                )
                    else:
                        schedule.append(
                            _add_course_with_sections(course, num_sections)
                        )

        elif "major_related_paths" in details:
            # Process major paths
            for path in details["major_related_paths"]["paths"]:
                for sub_course in path["courses"]:
                    schedule.append(
                        _add_course_with_sections(sub_course, num_sections)
                    )

    return schedule


def _add_course_with_sections(
    course: Dict[str, Any],
    num_sections: int,
) -> Dict[str, Any]:
    """
    Add section information to a course.

    Args:
        course: Course dictionary with 'course' and 'credits' keys
        num_sections: Number of sections to generate

    Returns:
        Course dictionary with added 'sections' list
    """
    sections = []

    for section_id in range(1, num_sections + 1):
        # Randomly choose between MWF and TTh schedules
        if random.choice([True, False]):
            time_slot = random.choice(MWF_TIME_SLOTS)
            day_type = "MWF"
        else:
            time_slot = random.choice(TTH_TIME_SLOTS)
            day_type = "TTh"

        sections.append(
            {
                "section_id": section_id,
                "day_type": day_type,
                "time_slot": time_slot,
            }
        )

    # Create a copy to avoid modifying original
    course_with_sections = course.copy()
    course_with_sections["sections"] = sections

    return course_with_sections


def load_course_data(file_path: str) -> Dict[str, Any]:
    """
    Load course data from JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed course data dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Course data file not found: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info("Loaded course data from: %s", file_path)
    return data


def save_schedule(
    schedule: List[Dict[str, Any]],
    output_path: str = "data/class_schedule.json",
) -> None:
    """
    Save generated schedule to JSON file.

    Args:
        schedule: List of courses with sections
        output_path: Path where schedule should be saved
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

    logger.info("Schedule saved to: %s (total courses: %d)", output_path, len(schedule))


def main() -> None:
    """Main entry point for class schedule generation."""
    logging.basicConfig(level=logging.INFO)

    # Load course structure
    try:
        course_data = load_course_data("data/course_structure.json")
    except FileNotFoundError:
        logger.error(
            "Course structure file not found. "
            "Run preprocess.py first to generate it."
        )
        return

    # Generate schedule with time slots
    logger.info("Generating class schedule with time slots...")
    schedule = generate_schedule_with_times(course_data, num_sections=3)

    # Save to file
    save_schedule(schedule)

    print(f"✅ Generated schedule with {len(schedule)} courses")
    print("   Saved to: data/class_schedule.json")


if __name__ == "__main__":
    main()
