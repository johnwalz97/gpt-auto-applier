import os
import re
import sys

import dotenv
import openai
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load environment variables
dotenv.load_dotenv()
# setup OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_job_description(soup: BeautifulSoup) -> str:
    """Extract the job description from the page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.
    Returns:
        str: The job description.
    """
    text = soup.get_text()
    return "".join([s for s in text.strip().splitlines(True) if s.strip()])


def should_navigate_to_form(soup: BeautifulSoup) -> str:
    """Check if the page contains a link to an application form.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.
    Returns:
        str: The link to the application form.
    """
    links = soup.find_all(["a"], string=re.compile("apply|submit", re.IGNORECASE))

    if not links:
        return None

    link = links[0]
    if link["href"].startswith("#"):
        return None

    return link["href"]


def extract_form_fields(soup: BeautifulSoup) -> list:
    """Extract the form fields from the page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.
    Returns:
        list: The form fields.
    """
    forms = soup.find_all("form")

    if not forms:
        raise Exception("No form found on page")

    if len(forms) > 1:
        raise Exception("Multiple forms found on page")

    return [input.prettify() for input in forms[0].find_all("input")]


def get_form_completion(
        form_fields: list,
        resume_data: str,
        personal_info: str,
    ) -> dict:
    """Get the form completion from OpenAI.

    Args:
        form_fields (list): The form fields.
        resume_data (str): The resume data.
        personal_info (str): The personal info.
    Returns:
        dict: The form completion.
    """
    prompt = f"""
    Using the following resume and personal info:
    RESUME={resume_data}
    PERSONAL_INFO={personal_info}
    
    fill in the following form fields:
    {', '.join(form_fields)}
    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    filled_form_fields = response.choices[0].text.strip().split("\n")
    return {
        field: value
        for field, value in (entry.split(": ") for entry in filled_form_fields)
    }


def generate_cover_letter(
        resume_data: str,
        job_description: str,
        job_requirements: str,
    ) -> str:
    """Generate a cover letter using OpenAI.

    Args:
        resume_data (str): The resume data.
        job_description (str): The job description.
        job_requirements (str): The job requirements.
    Returns:
        str: The cover letter.
    """
    prompt = f"""
    Create a cover letter using the following resume data:
    {resume_data}
    and the job description:
    {job_description}
    and the job requirements:
    {job_requirements}
    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def main(job_urls: list, resume_data: str, personal_info: str):
    """Main function.

    Args:
        job_urls (list): The job urls.
        resume_data (str): The resume data.
        personal_info (str): The personal info.
    """
    driver = webdriver.Chrome()

    for url in job_urls:
        jd_page = requests.get(url)
        soup = BeautifulSoup(jd_page.text, "html.parser")

        job_description = extract_job_description(soup)
        application_form_url = should_navigate_to_form(soup)

        if application_form_url:
            driver.get(application_form_url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        else:
            driver.get(url)

        form_fields = extract_form_fields(soup)
        fields_to_fill = get_form_completion(form_fields, resume_data, personal_info)

        print(fields_to_fill)


if __name__ == "__main__":
    job_urls = [
        "https://some-link.com/job/123",
    ]

    resume_path = sys.argv[1] if len(sys.argv) > 1 else "resume.pdf"
    if not os.path.exists(resume_path):
        print("Please provide a valid path to your resume.")
        sys.exit()
    if resume_path.endswith(".pdf"):
        with open(resume_path, "rb") as f:
            resume_data = PdfFileReader(f).getPage(0).extractText()
    elif resume_path.endswith(".txt"):
        with open(resume_path, "r") as f:
            resume_data = f.read()
    else:
        print("Please provide a valid pdf or text file path for your resume.")
        sys.exit()

    personal_info = """
    NAME=John Doe
    EMAIL=johndoe@gmail.com
    PHONE=1234567890
    COUNTRY=United States
    CITY=Tampa
    STATE=Florida
    ZIP=12345
    ADDRESS=123 Main St
    WORK_AUTHORIZATION=US Citizen
    ADDTL=I am a US Citizen and I am authorized to work in the US without sponsorship
    START_DATE=ASAP
    GITHUB=https://github.com/johndoe
    LINKEDIN=https://www.linkedin.com/in/johndoe
    DISABLED=No
    VETERAN=No
    GENDER=Male
    """

    main(job_urls, resume_data, personal_info)
