import gradio as gr
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from openai import OpenAI
import time
from docx import Document
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv(override=True)

# LinkedIn logo as an SVG string
LINKEDIN_LOGO = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="50" height="50">
    <path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z"/>
</svg>
"""

class LinkedInJDScraper:
    def __init__(self, email, password):
        """Initialize the LinkedIn scraper with credentials"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # Run in headless mode for Gradio
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.email = email
        self.password = password
    
    def login(self):
        """Login to LinkedIn"""
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(3)
            return True
            
        except Exception as e:
            return f"Login failed: {str(e)}"
    
    def get_description(self, job_url):
        """Scrape job description from LinkedIn"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.driver.get(job_url)
                
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-description"))
                )
                
                try:
                    show_more = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button.show-more-less-html__button"))
                    )
                    if show_more.is_displayed():
                        show_more.click()
                        time.sleep(1)
                except (TimeoutException, NoSuchElementException):
                    pass
                
                description_element = self.driver.find_element(By.CSS_SELECTOR, "div.jobs-description")
                description = description_element.text
                
                if description:
                    start_index = description.lower().find("about the job")
                    if start_index != -1:
                        return description[start_index:]
                    return description
                
                retry_count += 1
                time.sleep(2)
                
            except Exception as e:
                retry_count += 1
                time.sleep(2)
                
        return "Failed to retrieve job description after multiple attempts"
    
    def close(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except:
            pass

def read_resume(file_obj):
    """Read resume content from uploaded file"""
    try:
        # Get the file path directly from the Gradio file object
        file_path = file_obj.name
        
        # Read the document directly from the path
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text.strip())
        
        return "\n".join(text)
    except Exception as e:
        return f"Error reading resume: {str(e)}"


def generate_cover_letter(linkedin_email, linkedin_password, job_url, resume_file):
    """Generate cover letter based on job description and resume"""
    
    # Input validation
    if not all([linkedin_email, linkedin_password, job_url]):
        return "Please fill in all required fields (LinkedIn email, password, and job URL)"
    
    if not resume_file:
        return "Please upload a resume file"
    
    try:
        # Initialize scraper and get job description
        scraper = LinkedInJDScraper(linkedin_email, linkedin_password)
        login_result = scraper.login()
        
        if isinstance(login_result, str) and "failed" in login_result.lower():
            scraper.close()
            return login_result
        
        # Get job description
        job_description = scraper.get_description(job_url)
        scraper.close()
        
        if "Failed to retrieve" in job_description:
            return job_description
        
        # Read resume
        resume_content = read_resume(resume_file)
        if "Error reading resume" in resume_content:
            return resume_content
        
        # Prepare prompts
        system_prompt = """
        You are a career assistant specialized in crafting professional and personalized cover letters. 
        Your goal is to create compelling, tailored cover letters that align with the job description. 
        Each cover letter should emphasize the user's qualifications, skills, and experiences while maintaining a professional tone and structure.
        """
        
        user_prompt = f"""
        Create a professional cover letter based on:
        
        Resume content:
        {resume_content}
        
        Job Description:
        {job_description}
        
        Make the cover letter specific to the role and highlight relevant experience.
        """
        
        # Generate cover letter using OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "OpenAI API key not found. Please check your .env file."
            
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"
    finally:
        # Ensure browser is closed
        if 'scraper' in locals():
            scraper.close()

def create_gradio_interface():
    """Create and configure the Gradio interface"""
    with gr.Blocks(title="LinkedIn Cover Letter Generator") as app:
        # Header with logo and title
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML(LINKEDIN_LOGO)
            with gr.Column(scale=4):
                gr.Markdown("# LinkedIn Cover Letter Generator")
        
        with gr.Row():
            with gr.Column():
                linkedin_email = gr.Textbox(
                    label="LinkedIn Email",
                    placeholder="Enter your LinkedIn email"
                )
                linkedin_password = gr.Textbox(
                    label="LinkedIn Password",
                    type="password",
                    placeholder="Enter your LinkedIn password"
                )
                job_url = gr.Textbox(
                    label="LinkedIn Job URL",
                    placeholder="Paste the LinkedIn job posting URL"
                )
                resume_file = gr.File(
                    label="Upload Resume (DOCX)",
                    file_types=[".docx"]
                )
                
                generate_button = gr.Button("Generate Cover Letter", variant="primary")
            
            with gr.Column():
                output = gr.Markdown(label="Generated Cover Letter")
        
        generate_button.click(
            fn=generate_cover_letter,
            inputs=[linkedin_email, linkedin_password, job_url, resume_file],
            outputs=output
        )
    
    return app

# Main execution
if __name__ == "__main__":
    # Create and launch the Gradio app
    app = create_gradio_interface()
    app.launch(share=True)