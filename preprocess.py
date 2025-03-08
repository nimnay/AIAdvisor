# Script for preprocessing PDF catalog data
# For now I will focus on catalog year: 2024/2025
import pdfplumber

pdf_path = "/Users/angiediaz/Downloads/catalog2425.pdf"

text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Save the extracted text for analysis
with open("catalog_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Text extraction complete!")


# now we extract based on the infor in the text file
import json

data = {
    "general_education": {
        "arts_and_humanities": [
            {"course": "Arts and Humanities (Non-Literature)", "credits": 3, "semester": "First Semester - Second Year"},
            {"course": "Arts and Humanities (Literature)", "credits": 3, "semester": "First Semester - Sophomore Year"}
        ],
        "natural_science": [
            {"course": "Natural Science Requirement", "credits": 4, "semester": "First Semester - Freshman Year"},
            {"course": "Natural Science Requirement", "credits": 4, "semester": "Second Semester - Freshman Year"}
        ],
        "oral_communication": [
            {"course": "Oral Communication Requirement", "credits": 3, "semester": "First Semester - Sophomore Year"}
        ],
        "social_science": [
            {"course": "Social Science Requirement", "credits": 3, "semester": "First Semester - Junior Year"},
            {"course": "Social Science Requirement", "credits": 3, "semester": "Second Semester - Junior Year"}
        ],
        "global_challenges": [
            {"course": "Global Challenges Requirement", "credits": 3, "semester": "First Semester - Junior Year"},
            {"course": "Global Challenges Requirement", "credits": 3, "semester": "Second Semester - Senior Year"}
        ],
        "writing": [
            {"course": "Writing Requirement", "credits": 3, "semester": "First Semester - Senior Year"}
        ]
    },
    "major_related_classes": {
        "first_year": [
            {"course": "ENGL 1030 - Composition and Rhetoric", "credits": 3, "semester": "First Semester - Freshman Year"},
            {"course": "MATH 1060 - Calculus of One Variable I", "credits": 4, "semester": "First Semester - Freshman Year"},
            {"course": "MATH 1080 - Calculus of One Variable II", "credits": 4, "semester": "Second Semester - Freshman Year"}
        ],
        "sophomore_year": [
            {"course": "CPSC 2070 - Discrete Structures for Computing", "credits": 3, "semester": "First Semester - Sophomore Year", "prereq": ["MATH 1060"]},
            {"course": "CPSC 2120 - Algorithms and Data Structures", "credits": 4, "semester": "First Semester - Sophomore Year", "prereq": ["CPSC 2070"]},
            {"course": "CPSC 2150 - Software Development Foundations", "credits": 3, "semester": "Second Semester - Sophomore Year", "prereq": ["CPSC 2120"]},
            {"course": "CPSC 2310 - Introduction to Computer Organization", "credits": 4, "semester": "Second Semester - Sophomore Year", "prereq": ["CPSC 2120"]}
        ],
        "junior_year": [
            {"course": "CPSC 3720 - Introduction to Software Engineering", "credits": 3, "semester": "First Semester - Junior Year", "prereq": ["CPSC 2120"]},
            {"course": "CPSC 3220 - Advanced Systems", "credits": 3, "semester": "First Semester - Junior Year", "prereq": ["CPSC 2120"]},
            {"course": "CPSC 4030 - Data Science and Artificial Intelligence", "credits": 3, "semester": "Second Semester - Junior Year", "prereq": ["CPSC 2120"]}
        ],
        "senior_year": [
            {"course": "CPSC 4910 - Senior Computing Practicum", "credits": 3, "semester": "Second Semester - Senior Year", "prereq": ["CPSC 3720"]},
            {"course": "CPSC 3520 - Programming Systems", "credits": 3, "semester": "First Semester - Senior Year", "prereq": ["CPSC 3720"]}
        ]
    },
    "credits": {
        "total_credits": 122,
        "semester_credits": {
            "freshman_year": {
                "first_semester": 15,
                "second_semester": 15
            },
            "sophomore_year": {
                "first_semester": 16,
                "second_semester": 16
            },
            "junior_year": {
                "first_semester": 15,
                "second_semester": 15
            },
            "senior_year": {
                "first_semester": 15,
                "second_semester": 15
            }
        }
    }
}

# Saving the data to a JSON file
with open('course_structure.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file 'course_structure.json' has been created!")


