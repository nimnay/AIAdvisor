# Script for preprocessing PDF catalog data
# For now I will focus on catalog year: 2024/2025
import pdfplumber

pdf_path = "/Users/angiediaz/Downloads/catalog24:25.pdf"

text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Save the extracted text for analysis
with open("catalog_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Text extraction complete!")