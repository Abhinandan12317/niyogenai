from data import db, User, Job
from app import app
import os
import shutil

RECRUITER_UPLOAD_PATH = os.path.join(os.getcwd(), 'Data', 'Recruiter')
CLIENT_UPLOAD_PATH = os.path.join(os.getcwd(), 'Data', 'Client')

def clear_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)

with app.app_context():
    db.drop_all()
    db.create_all()
    clear_directory(RECRUITER_UPLOAD_PATH)
    clear_directory(CLIENT_UPLOAD_PATH)
    print('Database and uploaded files cleared')