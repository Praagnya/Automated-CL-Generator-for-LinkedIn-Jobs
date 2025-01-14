
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from dotenv import load_dotenv

class LinkedInJDScraper:
    def __init__(self, email, password):
        # Initialize the Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.email = email
        self.password = password

    def login(self):
        # Login to LinkedIn
        try:
            self.driver.get("https://www.linkedin.com/login")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            self.driver.find_element(By.ID, "username").send_keys(self.email)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        except TimeoutException:
            print("Login page did not load in time.")

    def scrape_job_descriptions(self, job_urls):
        # Scrape job descriptions from provided LinkedIn job URLs
        job_descriptions = {}
        for url in job_urls:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-description-content"))
                )
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                description = soup.find("div", class_="jobs-description-content").get_text(strip=True)
                job_descriptions[url] = description
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error scraping {url}: {e}")
                job_descriptions[url] = None
        return job_descriptions

    def close(self):
        # Close the WebDriver
        self.driver.quit()

if __name__ == "__main__":
    load_dotenv()
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    # Example usage
    scraper = LinkedInJDScraper(email, password)
    scraper.login()
    job_urls = [
        "https://www.linkedin.com/jobs/view/4123644034", # Add your LinkedIn job ID only here
    ]
    job_descriptions = scraper.scrape_job_descriptions(job_urls)
    print(job_descriptions)
    scraper.close()
