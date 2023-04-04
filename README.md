# Job Application AutoFill Using GPT-3

This project is a technical demo and not intended for actual use. I did this for fun and to learn more about GPT-3. I am not responsible for any misuse of this code.

This project aims to automate the process of filling out job applications using OpenAI's GPT-3. It takes a list of job URLs, navigates to the application form, extracts the form fields, and fills them out intelligently using GPT-3 based on the provided resume and personal information. Additionally, it generates a short, relevant cover letter using GPT-3.

## Features

- Extract job description and requirements
- Navigate to application form
- Extract form fields
- Fill out form fields using GPT-3
- Generate a cover letter using GPT-3

## Installation

1. Clone this repository:

```bash
git clone https://github.com/johnwalz97/gpt-auto-applier.git
cd gpt-auto-applier
```

2. Install the required dependencies:

This repo uses Poetry to handle deps and virtualenvs. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). Once Poetry is installed, run the following command to install the dependencies:

```bash
poetry install
```

3. Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
OPENAI_API_KEY=<your OpenAI API key>
```

## Usage

1. Create a `resume.txt` file in the root directory of the project. This file should contain your resume in plain text format.

2. Fill in the personal info in the auto_applier.py file:

3. Run the script:

```bash
poetry run python auto_applier.py
```
