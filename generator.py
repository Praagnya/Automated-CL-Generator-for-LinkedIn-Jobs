
import os
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

class CVGenerator:
    def __init__(self):
        # Load API key for OpenAI
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set it in the .env file.")
        self.model = OpenAI(api_key=self.api_key)

    def generate_cv(self, job_description, user_details):
        """
        Generates a tailored CV based on the job description and user details.

        :param job_description: Text of the job description.
        :param user_details: Dictionary containing user information (name, skills, experience, etc.).
        :return: A formatted CV as a string.
        """
        prompt = f"""
        Create a tailored CV for the following job description and user details:
        
        Job Description:
        {job_description}
        
        User Details:
        {user_details}
        
        The CV should be professional and formatted for ATS (Applicant Tracking Systems). Include the following sections:
        - Contact Information
        - Professional Summary
        - Skills
        - Work Experience
        - Education
        - Certifications (if any)
        - References (if provided)
        """
        
        response = self.model.generate(prompt, model="gpt-4", max_tokens=1500)
        return response.get("choices")[0].get("text").strip()

    def save_cv(self, cv_text, file_name="Tailored_CV.docx"):
        """
        Saves the CV text to a Word document.

        :param cv_text: The CV content as plain text.
        :param file_name: The name of the file to save the CV.
        """
        doc = Document()
        doc.add_paragraph(cv_text)
        doc.save(file_name)
        print(f"CV saved as {file_name}")

if __name__ == "__main__":
    # Example usage
    generator = CVGenerator()

    # Sample job description and user details
    job_description = "We are looking for a data scientist skilled in Python, machine learning, and data visualization."
    user_details = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "skills": ["Python", "Machine Learning", "Data Visualization", "SQL", "R"],
        "experience": [
            {
                "title": "Data Analyst",
                "company": "ABC Corp",
                "duration": "Jan 2020 - Dec 2022",
                "responsibilities": [
                    "Analyzed large datasets to generate actionable insights.",
                    "Developed predictive models to optimize business processes."
                ]
            }
        ],
        "education": "M.S. in Data Science, XYZ University",
        "certifications": ["Certified Data Scientist"],
    }

    # Generate and save the CV
    cv_text = generator.generate_cv(job_description, user_details)
    generator.save_cv(cv_text)
