def get_cl_user_prompt_with_scraped_jd(job_url, scraper, resume_skills):
    # Scrape job description
    description = scraper.scrape_job_descriptions([job_url]).get(job_url)

    # Construct the prompt
    user_prompt = "You are tasked with creating a professional and tailored Cover Letter for a job application.\n"
    user_prompt += "Here is a list of skills and experiences from the candidate's resume:\n"
    user_prompt += f"{resume_skills}\n\n"
    user_prompt += "Here is the job description for the position they are applying for:\n"
    user_prompt += f"{description}\n\n"
    user_prompt += (
        "Using the skills from the candidate's resume, craft a CL that highlights their most relevant qualifications "
        "and experiences for this job making use of job description. "
        "Ensure the CV follows a professional format and aligns with the role requirements. Present the CV in markdown format.\n"
    )
    return user_prompt
