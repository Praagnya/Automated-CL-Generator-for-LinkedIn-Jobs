from docx import Document

def read_text_from_word(file_path):
    """Extracts and returns all text from a Word document."""
    # Load the document
    doc = Document(file_path)
    
    # Extract text from each paragraph
    text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():  # Skip empty lines
            text.append(paragraph.text.strip())
    
    return "\n".join(text)

file_path = "Sample_Resume.docx"  # Replace with your file path
resume_skills = read_text_from_word(file_path)

print(resume_skills)