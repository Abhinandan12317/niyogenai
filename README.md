# Resume Parser

## Overview
Resume Parser is a web application that allows users to parse and analyze resumes. It provides functionalities for recruiters and clients to upload job descriptions and resumes, and compare them to find the best candidates.

## Features
- Parse and analyze resumes
- Upload job descriptions
- Compare resumes with job descriptions
- User roles: Recruiter and Client

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/Resume-Parser-OpenAI.git
cd Resume-Parser-OpenAI
```

### 2. Install Required Libraries
```sh
pip install -r requirements.txt
```

### 3. Provide OpenAI API Key
Add your OpenAI API key in the .yaml file.

### 4. Run the Application
```sh
python app.py
```

Go to: https://localhost:8000

## Objective

Creating a resume parser app using Flask is a great way to help job seekers test the ATS (Applicant Tracking System) friendliness of their resumes. The app allows users to upload their resumes in PDF format, which are then parsed to extract various pieces of information such as full name, email ID, GitHub portfolio, LinkedIn ID, employment details, technical skills, and soft skills. The extracted information is then presented in JSON format, providing users with valuable insights into the effectiveness of their resumes.

To build such an app, you can leverage various tools and libraries, including Python, Flask, Pyresparser, pdfminer.six, docx2txt, and NLP (natural language processing) libraries such as nltk and spacy. These tools enable the extraction of essential information from resumes in PDF and DOCx formats, making the process automated and efficient.

The app's functionality aligns with the growing need for streamlined recruitment processes and the increasing reliance on technology to evaluate and process job applications. By providing users with a detailed analysis of their resumes, the app empowers job seekers to optimize their resumes for better visibility and compatibility with ATS.

### Sneak Peak of the App
![image](https://github.com/pik1989/Resume-Parser-OpenAI/assets/34673684/5d206207-1b25-4dbe-8e11-add701b632e7)

#### Overview: 
This App is created for job seekers to test whether their resumes are ATS friendly or not, if our App is able to parse your details and show it, then assume that everything is good.

#### Features: 
Ability to extract specific information from resumes, the use of JSON format for presenting the extracted data, and the integration of various libraries and tools for parsing resumes.

#### Installation: 
Run the pip install requirements.txt to install and set up the app, including any dependencies and prerequisites.

#### Usage: 
Just upload your resume in pdf format, and see for yourself :)


##### Running the program

1. Clone the repository to your local machine
2. Navigate to the project directory
3. Install all the required libraries (just run pip install -r /path/to/requirements.txt)
4. Provide your Open AI API key in the .yaml file
5. Run the following command to start the chatbot -

    ```
    python app.py
    ```

    ```
    Go to: https://localhost:8000
    ```
    
Overall, the development of a resume parser app using Flask represents a significant advancement in leveraging technology to support job seekers in optimizing their resumes for the modern recruitment landscape. This app aligns with the increasing demand for efficient and technology-driven solutions in the job application process, ultimately benefiting both job seekers and recruiters.
