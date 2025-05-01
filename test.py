from data import db, User, Job
from app import app

def display_database_contents():
    with app.app_context():
        users = User.query.all()
        jobs = Job.query.all()

        # Write Users to file
        with open("users.txt", "w") as user_file:
            if users:
                user_file.write("Users:\n")
                for user in users:
                    user_file.write(
                        f"ID: {user.id}, Name: {user.name}, Email: {user.email}, "
                        f"Qualification: {user.qualification}, Experience: {user.experience}, "
                        f"Skills: {user.skills}, Role: {user.role}\n"
                    )
            else:
                user_file.write("No users found in the database.\n")

        # Write Jobs to file
        with open("jobs.txt", "w") as job_file:
            if jobs:
                job_file.write("Jobs:\n")
                for job in jobs:
                    job_file.write(
                        f"ID: {job.id}, Title: {job.title}, Qualifications: {job.qualifications}, "
                        f"Description: {job.description}, Domain: {job.domain}, "
                        f"PDF Path: {job.pdf_path}\n"
                    )
            else:
                job_file.write("No jobs found in the database.\n")

if __name__ == "__main__":
    display_database_contents()





