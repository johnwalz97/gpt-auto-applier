import re

import requests
from bs4 import BeautifulSoup

URL = "https://boards.greenhouse.io/forgeglobal/jobs/4829973004?gh_src=425b048f4us"
# URL = "https://jobs.lever.co/vk/fa31f961-901a-4eab-b8fd-4c36ea696870?lever-source=LinkedInJobs"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# # just get text from the page
# text = soup.get_text()
# text = "".join([s for s in text.strip().splitlines(True) if s.strip()])
# print(text)

# find any buttons or links that say "apply" or "submit" (case-insensitive)
# print(soup.find_all(["button", "a"], string=re.compile("apply|submit", re.IGNORECASE)))

# get first form
form = soup.find("form")
# get all inputs from the form
inputs = form.find_all("input")
with open("raw.html", "w") as f:
    f.write(form.prettify())
