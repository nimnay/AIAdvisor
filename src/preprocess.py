"""Preprocessing utilities for extracting and structuring course catalog data."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract text content from a PDF catalog file.

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional path to save extracted text

    Returns:
        Extracted text content

    Raises:
        ImportError: If pdfplumber is not installed
        FileNotFoundError: If PDF file doesn't exist
    """
    try:
        import pdfplumber
    except ImportError:
        raise ImportError(
            "pdfplumber is required for PDF processing. "
            "Install it with: pip install pdfplumber"
        )

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    logger.info("Extracting text from PDF: %s", pdf_path)

    text_content = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text_content += page_text + "\n"
            if i % 10 == 0:
                logger.debug("Processed %d pages", i)

    # Save to file if output path specified
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(text_content, encoding="utf-8")
        logger.info("Saved extracted text to: %s", output_path)

    logger.info("Text extraction complete. Total characters: %d", len(text_content))
    return text_content


def create_course_structure() -> Dict[str, Any]:
    """
    Create the course structure data for Computer Science BS degree.

    Returns:
        Dictionary containing general education and major-specific courses
    """
    structure = {
        "general_education": {
            "arts_and_humanities": [
                {
                    "course": "Arts and Humanities (Non-Literature)",
                    "credits": 3,
                    "semester": "First Semester - Second Year",
                },
                {
                    "course": "Arts and Humanities (Literature)",
                    "credits": 3,
                    "semester": "First Semester - Sophomore Year",
                },
            ],
            "natural_science": [
                {
                    "course": "Natural Science Requirement",
                    "credits": 4,
                    "semester": "First Semester - Freshman Year",
                },
                {
                    "course": "Natural Science Requirement",
                    "credits": 4,
                    "semester": "Second Semester - Freshman Year",
                },
            ],
            "oral_communication": [
                {
                    "course": "Oral Communication Requirement",
                    "credits": 3,
                    "semester": "First Semester - Sophomore Year",
                }
            ],
            "social_science": [
                {
                    "course": "Social Science Requirement",
                    "credits": 3,
                    "semester": "First Semester - Junior Year",
                },
                {
                    "course": "Social Science Requirement",
                    "credits": 3,
                    "semester": "Second Semester - Junior Year",
                },
            ],
            "global_challenges": [
                {
                    "course": "Global Challenges Requirement",
                    "credits": 3,
                    "semester": "First Semester - Junior Year",
                },
                {
                    "course": "Global Challenges Requirement",
                    "credits": 3,
                    "semester": "Second Semester - Senior Year",
                },
            ],
            "writing": [
                {
                    "course": "Writing Requirement",
                    "credits": 3,
                    "semester": "First Semester - Senior Year",
                }
            ],
        },
        "general_education_classes": {
            "class_options": {
                "arts_and_humanities_non_lit": [
                    {"course": "MUSC 2100 - Music in the Western World", "credits": 3},
                    {"course": "THEA 2100 - Theatre Appreciation", "credits": 3},
                    {"course": "ARTS 2100 - Art Appreciation", "credits": 3},
                ],
                "arts_and_humanities_lit": [
                    {"course": "ENGL 2120 - World Literature", "credits": 3},
                    {"course": "ENGL 2130 - British Literature", "credits": 3},
                    {"course": "ENGL 2140 - American Literature", "credits": 3},
                ],
                "oral_communication_requirement": [
                    {
                        "course": "COMM 1500 - Introduction to Human Communication",
                        "credits": 3,
                    },
                    {"course": "COMM 2500 - Public Speaking", "credits": 3},
                    {"course": "ENGL 1030 - Composition and Rhetoric", "credits": 3},
                ],
                "natural_science_with_lab": [
                    {
                        "path_name": "BIOL 1030/1050",
                        "courses": [
                            {"course": "BIOL 1030 - General Biology I", "credits": 3},
                            {"course": "BIOL 1050 - General Biology Lab", "credits": 1},
                        ],
                    },
                    {
                        "path_name": "CH 1010/1011",
                        "courses": [
                            {"course": "CH 1010 - General Chemistry", "credits": 4},
                            {"course": "CH 1011 - General Chemistry Lab", "credits": 0},
                        ],
                    },
                    {
                        "path_name": "PHYS 1220/1240",
                        "courses": [
                            {
                                "course": "PHYS 1220 - Physics with Calculus I",
                                "credits": 3,
                            },
                            {"course": "PHYS 1240 - Physics Laboratory I", "credits": 1},
                        ],
                    },
                ],
                "social_sciences": [
                    {
                        "course": "ANTH 2010 - Introduction to Anthropology",
                        "credits": 3,
                    },
                    {"course": "GEOG 1010 - Introduction to Geography", "credits": 3},
                    {
                        "course": "POSC 1010 - American National Government",
                        "credits": 3,
                    },
                ],
                "global_challenges": [
                    {"course": "ENGL 2120 - World Literature", "credits": 3},
                    {"course": "ENGL 2130 - British Literature", "credits": 3},
                    {"course": "ENGL 2140 - American Literature", "credits": 3},
                ],
                "cross_cultural_awareness": [
                    {"course": "MUSC 3140 - World Music", "credits": 3}
                ],
                "science_and_technology_in_society": [
                    {
                        "course": "ENGR 2210 - Technology, Culture and Design",
                        "credits": 3,
                    }
                ],
                "mathematics": [
                    {
                        "course": "MATH 1060 - Calculus of One Variable I",
                        "credits": 4,
                    },
                    {
                        "course": "MATH 1080 - Calculus of One Variable II",
                        "credits": 4,
                    },
                ],
            }
        },
        "major_related_classes": {
            "first_year": [
                {
                    "course": "ENGL 1030 - Composition and Rhetoric",
                    "credits": 3,
                    "semester": "First Semester - Freshman Year",
                },
                {
                    "course": "MATH 1060 - Calculus of One Variable I",
                    "credits": 4,
                    "semester": "First Semester - Freshman Year",
                },
                {
                    "course": "MATH 1080 - Calculus of One Variable II",
                    "credits": 4,
                    "semester": "Second Semester - Freshman Year",
                },
                {
                    "course": "Introduction to Computing Requirement",
                    "credits": 4,
                    "semester": "First/Second Semester - Freshman Year",
                    "paths": [
                        {
                            "path_name": "CPSC 1010/1020",
                            "courses": [
                                {
                                    "course": "CPSC 1010 - Introduction to Computing I",
                                    "credits": 4,
                                },
                                {
                                    "course": "CPSC 1020 - Introduction to Computing II",
                                    "credits": 4,
                                },
                            ],
                        },
                        {
                            "path_name": "CPSC 1060/1070",
                            "courses": [
                                {
                                    "course": "CPSC 1060 - Introduction to Programming",
                                    "credits": 4,
                                },
                                {
                                    "course": "CPSC 1070 - Programming Methodology",
                                    "credits": 4,
                                },
                            ],
                        },
                    ],
                },
            ],
            "sophomore_year": [
                {
                    "course": "CPSC 2070 - Discrete Structures for Computing",
                    "credits": 3,
                    "semester": "First Semester - Sophomore Year",
                    "prereq": ["MATH 1060"],
                },
                {
                    "course": "CPSC 2120 - Algorithms and Data Structures",
                    "credits": 4,
                    "semester": "First Semester - Sophomore Year",
                    "prereq": ["CPSC 2070"],
                },
                {
                    "course": "CPSC 2150 - Software Development Foundations",
                    "credits": 3,
                    "semester": "Second Semester - Sophomore Year",
                    "prereq": ["CPSC 2120"],
                },
                {
                    "course": "CPSC 2310 - Introduction to Computer Organization",
                    "credits": 4,
                    "semester": "Second Semester - Sophomore Year",
                    "prereq": ["CPSC 2120"],
                },
            ],
            "junior_year": [
                {
                    "course": "CPSC 3720 - Introduction to Software Engineering",
                    "credits": 3,
                    "semester": "First Semester - Junior Year",
                    "prereq": ["CPSC 2120"],
                },
                {
                    "course": "CPSC 3220 - Advanced Systems",
                    "credits": 3,
                    "semester": "First Semester - Junior Year",
                    "prereq": ["CPSC 2120"],
                },
                {
                    "course": "CPSC 4030 - Data Science and Artificial Intelligence",
                    "credits": 3,
                    "semester": "Second Semester - Junior Year",
                    "prereq": ["CPSC 2120"],
                },
            ],
            "senior_year": [
                {
                    "course": "CPSC 4910 - Senior Computing Practicum",
                    "credits": 3,
                    "semester": "Second Semester - Senior Year",
                    "prereq": ["CPSC 3720"],
                },
                {
                    "course": "CPSC 3520 - Programming Systems",
                    "credits": 3,
                    "semester": "First Semester - Senior Year",
                    "prereq": ["CPSC 3720"],
                },
            ],
        },
        "major_related_paths": {
            "course": "Computer Science Path Requirement",
            "credits": 6,
            "semester": "Second Semester - Junior and Senior Year",
            "paths": [
                {
                    "path_name": "Advanced Systems",
                    "courses": [
                        {
                            "course": "CPSC 3220 - Introduction to Operating Systems",
                            "credits": 3,
                        },
                        {"course": "CPSC 3600 - Network Programming", "credits": 3},
                    ],
                },
                {
                    "path_name": "Intelligent Computing",
                    "courses": [
                        {
                            "course": "CPSC 4030 - Machine Learning",
                            "credits": 3,
                        },
                        {
                            "course": "CPSC 4300 - Artificial Intelligence",
                            "credits": 3,
                        },
                    ],
                },
                {
                    "path_name": "Interactive Systems",
                    "courses": [
                        {
                            "course": "CPSC 3750 - Human-Computer Interaction",
                            "credits": 3,
                        },
                        {"course": "CPSC 4110 - Game Development", "credits": 3},
                    ],
                },
            ],
        },
    }

    return structure


def save_course_structure(output_path: str = "data/course_structure.json") -> None:
    """
    Save course structure to JSON file.

    Args:
        output_path: Path where JSON file should be saved
    """
    structure = create_course_structure()

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    logger.info("Course structure saved to: %s", output_path)


def main() -> None:
    """Main preprocessing workflow."""
    logging.basicConfig(level=logging.INFO)

    # Example: Extract text from PDF (uncomment and update path as needed)
    # pdf_path = "path/to/catalog2425.pdf"
    # extract_text_from_pdf(pdf_path, "data/catalog_text.txt")

    # Generate and save course structure
    save_course_structure()
    print("✅ Course structure saved to data/course_structure.json")


if __name__ == "__main__":
    main()
