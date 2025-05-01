from flask import Flask, request, render_template, redirect, url_for, session, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import requests
from data import db, User, Job, Application  # Import Application model
import sys
import shutil
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.abspath(os.getcwd()))

RECRUITER_UPLOAD_PATH = os.path.join(os.getcwd(), 'Data', 'Recruiter')
CLIENT_UPLOAD_PATH = os.path.join(os.getcwd(), 'Data', 'Client')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECRUITER_UPLOAD_FOLDER'] = RECRUITER_UPLOAD_PATH
app.config['CLIENT_UPLOAD_FOLDER'] = CLIENT_UPLOAD_PATH
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Ensure the upload directories exist
os.makedirs(RECRUITER_UPLOAD_PATH, exist_ok=True)
os.makedirs(CLIENT_UPLOAD_PATH, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            # Store user details in the session
            session['user'] = {
                'email': email,
                'name': user.name,  # Store the user's name
                'role': user.role   # Store the user's role
            }
            return redirect(url_for('selectrole'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/recruiter')
def recruiter():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('recruiter.html')

@app.route('/client')
def client():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('client.html')

@app.route('/submit_job', methods=['POST'])
def submit_job():
    title = request.form['title']
    qualifications = request.form['qualifications']
    description = request.form['description']
    domain = request.form['domain']
    pdf = request.files['pdf']
    pdf_filename = pdf.filename
    pdf_path = os.path.join(app.config['RECRUITER_UPLOAD_FOLDER'], pdf_filename)
    pdf.save(pdf_path)
    new_job = Job(title=title, qualifications=qualifications, description=description, domain=domain, pdf_path=pdf_filename)
    db.session.add(new_job)
    db.session.commit()
    return redirect(url_for('recruiter'))

@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.title = request.form['title']
        job.qualifications = request.form['qualifications']
        job.description = request.form['description']
        job.domain = request.form['domain']
        if 'pdf' in request.files:
            pdf = request.files['pdf']
            if pdf.filename != '':
                # Delete the old PDF file
                old_pdf_path = os.path.join(app.config['RECRUITER_UPLOAD_FOLDER'], job.pdf_path)
                if os.path.exists(old_pdf_path):
                    os.remove(old_pdf_path)
                # Save the new PDF file
                pdf_filename = pdf.filename
                pdf_path = os.path.join(app.config['RECRUITER_UPLOAD_FOLDER'], pdf_filename)
                pdf.save(pdf_path)
                job.pdf_path = pdf_filename
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({
        'id': job.id,
        'title': job.title,
        'qualifications': job.qualifications,
        'description': job.description,
        'domain': job.domain,
        'pdf_path': job.pdf_path
    })

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    # Delete the PDF file
    pdf_path = os.path.join(app.config['RECRUITER_UPLOAD_FOLDER'], job.pdf_path)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/tokensignin', methods=['POST'])
def tokensignin():
    id_token = request.form['idtoken']
    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
    if response.status_code == 200:
        user_info = response.json()
        email = user_info['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create a new user with the email and no password
            user = User(email=email, password='', name='')  # Set default name to empty string
            db.session.add(user)
            db.session.commit()
        session['user'] = {'email': email, 'name': user.name, 'role': user.role}
        return redirect(url_for('selectrole'))
    else:
        return 'failure', 401

@app.route('/selectrole', methods=['GET', 'POST'])
def selectrole():
    if 'user' in session:
        email = session['user']['email']
        user = User.query.filter_by(email=email).first()
        if user and user.role:
            return redirect(url_for(user.role))
        if request.method == 'POST':
            name = request.form['name']
            qualification = request.form['qualification']
            experience = request.form['experience']  # Updated field
            skills = request.form['skills']
            role = request.form['role']
            if user:
                user.name = name
                user.qualification = qualification
                user.experience = experience  # Updated field
                user.skills = skills
                user.role = role
                db.session.commit()
                session['user']['name'] = name  # Update session with the new name
                session['user']['role'] = role  # Update session with the new role
                return redirect(url_for(role))
            else:
                return 'User not found', 404
        return render_template('selectrole.html')
    return redirect(url_for('login'))

@app.route('/jobs')
def jobs():
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for('login'))

    domain = request.args.get('domain')
    if domain:
        jobs = Job.query.filter_by(domain=domain).order_by(Job.title).all()
    else:
        jobs = Job.query.order_by(Job.title).all()

    if user.role == 'recruiter':
        # For recruiter.html with Edit and Delete buttons
        job_cards = ''.join([
            f'''
            <div class="job-card bg-white shadow-lg rounded-xl p-6 mb-6 transition transform hover:-translate-y-1 hover:shadow-2xl">
                <p class="text-gray-600 mb-4"><strong>Job ID:</strong> {job.id}</p>
                <h3 class="job-title text-2xl font-semibold mb-2 text-gray-800">{job.title}</h3>
                <p class="text-gray-600 mb-2"><strong>Qualifications:</strong> {job.qualifications}</p>
                <p class="text-gray-600 mb-2"><strong>Description:</strong> {job.description}</p>
                <p class="text-gray-600 mb-4"><strong>Domain:</strong> {job.domain}</p>
                <div class="flex justify-between items-center">
                    <a href="/view_pdf/{job.pdf_path}" class="text-blue-600 hover:text-blue-800 transition">View PDF</a>
                    <button onclick="showEditJob('{job.id}')" class="bg-yellow-500 text-white px-4 py-2 rounded-md shadow hover:bg-yellow-600 transition">Edit</button>
                    <button onclick="deleteJob('{job.id}')" class="bg-red-500 text-white px-4 py-2 rounded-md shadow hover:bg-red-600 transition">Delete</button>
                </div>
            </div>
            '''
            for job in jobs
        ])
    else:
        # For client.html with Apply Now button
        job_cards = ''.join([
            f'''
            <div class="job-card bg-white shadow-lg rounded-xl p-6 mb-6 transition transform hover:-translate-y-1 hover:shadow-2xl">
                <h3 class="job-title text-2xl font-semibold mb-2 text-gray-800">{job.title}</h3>
                <p class="text-gray-600 mb-2"><strong>Qualifications:</strong> {job.qualifications}</p>
                <p class="text-gray-600 mb-2"><strong>Description:</strong> {job.description}</p>
                <p class="text-gray-600 mb-4"><strong>Domain:</strong> {job.domain}</p>
                <div class="flex justify-between items-center">
                    <a href="/view_pdf/{job.pdf_path}" class="text-blue-600 hover:text-blue-800 transition">View PDF</a>
                    <a href="/apply/{job.id}" class="bg-green-500 text-white px-4 py-2 rounded-md shadow hover:bg-green-600 transition">Apply Now</a>
                </div>
            </div>
            '''
            for job in jobs
        ])

    return job_cards

@app.route('/start_hiring/<int:job_id>')
def start_hiring(job_id):
    job = Job.query.get_or_404(job_id)
    # Fetch the candidates who have applied for this job
    applications = Application.query.filter_by(job_id=job_id).all()

    return render_template('start_hiring.html', job=job, applications=applications)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if request.method == 'POST':
        if 'user' not in session:
            return jsonify({'message': 'Please login to apply for jobs.'}), 403

        name = request.form['name']
        description = request.form['description']
        email = session['user']['email']
        resume = request.files['resume']
        resume_filename = f"{email}_{resume.filename}"
        job_directory = os.path.join(app.config['CLIENT_UPLOAD_FOLDER'], job.title)
        os.makedirs(job_directory, exist_ok=True)
        resume_path = os.path.join(job_directory, resume_filename)
        resume.save(resume_path)

        # Store application data in the database
        application = Application(job_id=job.id, name=name, description=description, resume_filename=resume_filename)
        db.session.add(application)
        db.session.commit()

        return jsonify({'success': True})

    return render_template('application.html', job_id=job_id)

@app.route('/view_pdf/<filename>')
def view_pdf(filename):
    return send_from_directory(app.config['RECRUITER_UPLOAD_FOLDER'], filename)

@app.route('/view_resume/<filename>')
def view_resume(filename):
    return send_from_directory(app.config['CLIENT_UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=10000)
    

