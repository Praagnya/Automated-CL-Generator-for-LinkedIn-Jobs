# Automated Cover Letter Generator for LinkedIn Jobs

This project automates the process of creating tailored Cover Letter for job applications by extracting job descriptions from LinkedIn and using a large language model to generate customized CVs. The project integrates web scraping, API calls, and AI-powered text generation to streamline and optimize the job application process.

### Features
	•	Automated Job Description Extraction: Scrapes job descriptions from LinkedIn using Selenium and BeautifulSoup for detailed and structured data collection.
	•	AI-Powered CV Generation: Leverages OpenAI’s GPT model to analyze job descriptions and create CVs that align with specific job requirements.
	•	Workflow Automation: Integrates various tools and frameworks to automate the end-to-end process.
	•	Customizable Outputs: Allows users to modify templates and input additional details for personalization.
	•	Error Handling: Implements robust exception handling and retry mechanisms to ensure smooth operation during web scraping and API calls.

### Technology Stack
	•	Programming Languages: Python
	•	Libraries and Frameworks:
	•	Web Scraping: Selenium, BeautifulSoup
	•	API Integration: openai
	•	Document Generation: python-docx
	•	Workflow Automation: APScheduler, argparse
	•	Deployment: Docker
	•	Version Control: GitHub
	•	Testing: unittest

### How It Works
	1.	Input: Provide LinkedIn job post URLs or search parameters.
	2.	Scraping: Extract job descriptions using Selenium for browser automation.
	3.	AI Processing: Use OpenAI’s GPT model to analyze the job description and generate a tailored CV.
	4.	Output: Save the CV as .docx and .pdf files in a specified directory.
	5.	Customization: Adjust templates or add personal details for enhanced CV alignment.

### Installation

Prerequisites
	•	Python 3.8+
	•	Chrome WebDriver (compatible with your Chrome browser version)
	•	OpenAI API Key

Steps
	1.	Clone the repository:

git clone https://github.com/yourusername/Automated-CV-Generator-for-LinkedIn-Jobs.git
cd Automated-CV-Generator-for-LinkedIn-Jobs


	2.	Install dependencies:

pip install -r requirements.txt


	3.	Set up environment variables:
	•	Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key
LINKEDIN_EMAIL_ID="your_email_id@example.com"
LINKEDIN_PASSWORD=*******

	4.	Run the script:

python main.py --url "https://www.linkedin.com/jobs/view/12345678"

Usage

Command-Line Arguments
	•	--url: URL of the LinkedIn job post (required).
	•	--output: Directory to save the CV (default: ./output).
	•	--template: Path to a custom CV template (optional).

Example:

python main.py --url "https://www.linkedin.com/jobs/view/12345678" --output "./output"

### Project Structure

File/Folder Descriptions
- **main.py**: The main script to run the project, orchestrating the entire workflow.
- **scraper.py**: Contains logic for extracting job descriptions from LinkedIn. It uses tools like Selenium or BeautifulSoup for web scraping.
- **user_prompt.py**: Manages the creation of structured prompts fed into AI models. These prompts format user skills and job descriptions for generating cover letters.
- **generator.py**: Utilizes AI models (e.g., OpenAI GPT) to create tailored Cover Letter based on the extracted job descriptions and user-provided data or resume.

Future Enhancements
	•	Add support for multiple job boards (e.g., Indeed, Glassdoor).
	•	Implement advanced analytics for CV optimization.
	•	Introduce a web interface for user interaction.
	•	Add multi-language support for job descriptions and CVs.

### Contributing

Contributions are welcome! Please follow the guidelines in CONTRIBUTING.md to submit bug reports, feature requests, or pull requests.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

If you have any questions or feedback, feel free to reach out:
	•	Email: praagnya@gmail.com / pnarasimha@arizona.edu

Let me know if you’d like additional details or modifications!
