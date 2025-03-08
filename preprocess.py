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
"""

import re
import json

# Read the extracted text
with open("catalog_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Find the CS Degree section
cs_section_start = text.find("Computer Science, BS")
cs_section_end = text.find("Computer Information Systems, BS")  # Stop before next major
cs_text = text[cs_section_start:cs_section_end]

# Extract course patterns like "CPSC 2120 - Algorithms and Data Structures"
course_pattern = re.findall(r"(CPSC \d{4}) - (.+?)\n", cs_text)

# Organize into categories (You'll refine this based on manual review)
cs_data = {
    "catalog_year": "2024-2025",
    "major": "Computer Science, BS",
    "degree_requirements": {
        "general_education": [],
        "core_courses": [],
        "electives": [],
        "prerequisites": {}
    }
}

for course_code, course_name in course_pattern:
    if "Introduction" in course_name or "Fundamentals" in course_name:
        cs_data["degree_requirements"]["general_education"].append(
            {"course_code": course_code, "course_name": course_name}
        )
    elif "Elective" in course_name:
        cs_data["degree_requirements"]["electives"].append(course_code)
    else:
        cs_data["degree_requirements"]["core_courses"].append(
            {"course_code": course_code, "course_name": course_name}
        )

# Save structured data
with open("cs_catalog_data.json", "w", encoding="utf-8") as json_file:
    json.dump(cs_data, json_file, indent=4)

print("Structured JSON file created!")

"""
