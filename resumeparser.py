import openai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from data import Application, Job  # Import database models from data.py

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
openai.api_key = api_key  # Set the OpenAI API key

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def compare_resume_with_job_description(resume_text, job_text):
    """Uses GPT to compare the resume with job requirements and return a similarity score."""
    system_message = "You are an expert HR assistant helping in recruitment."
    user_message = f"""
    Given the following candidate resume and job description, evaluate how well the candidate fits the job.
    Assign a relevance score from 0 to 100, where 100 means a perfect match and 0 means no match at all.
    
    Candidate Resume:
    {resume_text}
    
    Job Description:
    {job_text}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        score = response.choices[0].message["content"].strip()
        return int(score)
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

def get_resume_and_job_text(application_id):
    """Fetches resume and job description text from the database."""
    application = Application.query.get(application_id)
    if not application:
        print(f"Application with ID {application_id} not found.")
        return None, None
    
    job = Job.query.get(application.job_id)
    if not job:
        print(f"Job with ID {application.job_id} not found.")
        return None, None
    
    resume_path = os.path.join("Data", "Client", job.title, application.resume_filename)
    job_pdf_path = os.path.join("Data", "Recruiter", job.pdf_path)
    
    resume_text = extract_text_from_pdf(resume_path)
    job_text = extract_text_from_pdf(job_pdf_path)
    
    return resume_text, job_text

def main(application_id):
    """Main function to extract text and compare."""
    resume_text, job_text = get_resume_and_job_text(application_id)
    
    if not resume_text or not job_text:
        print("Error: Could not fetch resume or job description.")
        return
    
    score = compare_resume_with_job_description(resume_text, job_text)
    if score is not None:
        print(f"Candidate Relevance Score: {score}/100")
    else:
        print("Error: Could not calculate relevance score.")

if __name__ == "__main__":
    application_id = 1  # Change to actual application ID
    main(application_id)