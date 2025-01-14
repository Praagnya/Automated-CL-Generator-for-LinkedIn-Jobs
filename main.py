import os 
import requests 
import json 
from typing import List 
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup 
from IPython.display import Markdown, display, update_display 
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from docx import Document


# Initialize and constants
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10: 
    print("API key looks good so far") 
else: 
    print("There might be a problem with API key, Please Check") 

MODEL_GPT = 'gpt-4o-mini'
openai = OpenAI()

class LinkedInJDScraper:
    def __init__(self, email, password):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        # Add these options to prevent infinite loops
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)  # Reduced wait time
        self.email = email
        self.password = password
    
    def login(self):
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for email field with timeout
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            
            # Find password field
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Find and click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete with timeout
            time.sleep(3)
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def get_description(self, job_url):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Navigate to job page
                self.driver.get(job_url)
                
                # Wait for any description element to be present
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-description"))
                )
                
                # Try to click "Show more" if it exists
                try:
                    show_more = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button.show-more-less-html__button"))
                    )
                    if show_more.is_displayed():
                        show_more.click()
                        time.sleep(1)
                except (TimeoutException, NoSuchElementException):
                    pass
                
                # Get description text
                description_element = self.driver.find_element(By.CSS_SELECTOR, "div.jobs-description")
                description = description_element.text
                
                if description:
                    # Find start of job description
                    start_index = description.lower().find("about the job")
                    if start_index != -1:
                        return description[start_index:]
                    return description
                
                retry_count += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"Attempt {retry_count + 1} failed: {str(e)}")
                retry_count += 1
                time.sleep(2)
                
        return "Failed to retrieve job description after multiple attempts"
    
    def close(self):
        try:
            self.driver.quit()
        except:
            pass

if __name__ == "__main__":
    EMAIL = os.getenv('LINKEDIN_EMAIL')
    PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    
    scraper = LinkedInJDScraper(EMAIL, PASSWORD)
    
    try:
        if scraper.login():
            job_url = "https://www.linkedin.com/jobs/view/4109295398"
            description = scraper.get_description(job_url)
            print("\nJob Description:")
            print(description)
        else:
            print("Failed to login. Please check your credentials.")
    finally:
        scraper.close()

system_prompt = """
You are a career assistant specialized in crafting professional and personalized cover letters. 
Your goal is to create compelling, tailored cover letters that align with the job description. 
Each cover letter should emphasize the user’s qualifications, skills, and experiences while maintaining a professional tone and structure. 
Ensure the letter adheres to the following format:

1. **Introduction**: A brief and enthusiastic introduction expressing interest in the role and organization.
2. **Body**: Highlight relevant skills, experiences, and achievements that align with the job description. Use specific examples when possible.
3. **Closing**: Reiterate enthusiasm for the role, express willingness to contribute to the organization, and include a polite call to action.

Maintain clarity, professionalism, and conciseness while tailoring the letter. Don't add anything like as advertised.
"""


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

# Example Usage
file_path = "Sample_Resume.docx"  # Replace with your file path
resume_skills = read_text_from_word(file_path)

print(resume_skills)

def get_cl_user_prompt_with_scraped_jd(file_path, job_url, scraper):
    # Create the user prompt
    user_prompt = "You are tasked with creating a professional and tailored Cover Letter for a job application.\n"
    user_prompt += "Here is a list of skills and experiences from the candidate's resume:\n"
    user_prompt += f"{resume_skills}\n\n"
    user_prompt += "Here is the job description for the position they are applying for:\n"
    user_prompt += f"{description}\n\n"
    user_prompt += "Using the skills from the candidate's resume, craft a CL that highlights their most relevant qualifications and experiences for this job making use of job description. "
    user_prompt += "Ensure the CV follows a professional format and aligns with the role requirements. Present the CV in markdown format.\n"
    user_prompt = user_prompt 
    return user_prompt

def create_jd(system_prompt, file_path, job_url, scraper, model="gpt-4"):

        # OpenAI API call
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": get_cl_user_prompt_with_scraped_jd(file_path, job_url, scraper)}
            ]
        )

        # Extract and display the result
        result = completion.choices[0].message.content
        display(Markdown(result))

messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": get_cl_user_prompt_with_scraped_jd(file_path, job_url, scraper) }]
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
print(response.choices[0].message.content)

