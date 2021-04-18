from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Text
from sqlalchemy.orm import relationship 
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
import secrets
import os
import spacy
import json
import random
import en_core_web_sm
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
from functools import wraps


nlp = en_core_web_sm.load()

ner = nlp.get_pipe("ner")

TRAIN_RESUME_DATA = [
('Hello Hello', {
'entities': [(0, 11, 'DATE')]
})
]


ner.add_label('skills')

pipe_exceptions = ["ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

with nlp.disable_pipes(*unaffected_pipes):
    for iteration in range(20):
        random.shuffle(TRAIN_RESUME_DATA)
        for raw_text,entity_offsets in TRAIN_RESUME_DATA:
            resume=nlp.make_doc(raw_text)
            nlp.update([Example.from_dict(resume,entity_offsets)])

#resume = nlp("Dynamic individual with 6 years of software development experience in design, development, deployment, maintenance, production and support of web - based and Client-Server business ")

#for ent in resume.ents:
 #  print(ent.label_, ent.text)

ENV = 'dev'
   
app= Flask(__name__)

if ENV == 'dev':
     app.debug = True
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost/postgres'
else:
     app.debug = False
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kdtfxcdxnpszrq:c8dccd8f82d7b2f33d7da031caaf9e791ded57472c9ef082c7870b5527cc7a6e@ec2-34-252-251-16.eu-west-1.compute.amazonaws.com:5432/da7ukihqat8bgm'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ImageForm(FlaskForm):
    
    picture = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])

class ResumeForm(FlaskForm):
    
    resume = FileField('Update Resume', validators=[FileAllowed(['pdf', 'docx'])])

class InterviewForm(FlaskForm):

    entryDate = DateField('Interview Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    entryTime = TimeField('Interview Time', validators=(validators.DataRequired(),))

class Candidates(db.Model):
    __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    profile = db.Column(db.Text, nullable=False, default='No profile description added yet.')
    resume = db.Column(db.String(20))
    image_file = db.Column(db.String(20), nullable=False, default='profile_default.png')
    
    submissions = relationship("Submissions", backref="candidates")

    def __init__(self, firstname, lastname, phone, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.password = password

class Submissions(db.Model):
    __tablename__ = 'submissions'
    submission_id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer)
    resume_entities= db.Column(db.Text)
    candidate_id = db.Column(db.Integer, ForeignKey("candidates.candidate_id"))
    job_id = db.Column(db.Integer, ForeignKey("jobs.job_id"))
    employer_id = db.Column(db.Integer, ForeignKey("employers.employer_id"))
  
    def __init__(self, resume_entities, candidate_id, job_id, employer_id):
        self.result = result
        self.resume_entities = resume_entities
     
class Jobs(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    description_entities= db.Column(db.Text)

    submissions = relationship("Submissions", backref="jobs")

    def __init__(self, description_entities):
        self.description_entities = description_entities

class Adverts(db.Model):
    __tablename__ = 'adverts'
    advert_id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer)
    position = db.Column(db.String(255))
    experience = db.Column(db.Integer)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    candidates_number = db.Column(db.Integer)
    date = db.Column(db.Text)
    time = db.Column(db.Text)
    employer_id = db.Column(db.Integer, ForeignKey("employers.employer_id"))
    

    def __init__(self, salary, position, experience, location, description, candidate_number, date, time, employer_id):
        self.salary = salary
        self.position = position
        self.experience = experience
        self.location = location
        self.description = description
        self.candidates_number = candidate_number
        self.date = date
        self.time = time
        self.employer_id = employer_id

class Employers(db.Model):
    __tablename__ = 'employers'
    employer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    company = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255))
    profile = db.Column(db.Text, nullable=False, default='No profile description added yet.')
    image_file = db.Column(db.String(20), nullable=False, default='profile_default.png')
    
    submissions = relationship("Submissions", backref="employers")
    adverts = relationship("Adverts", backref="employers")

    def __init__(self, email, company, phone, password):
        self.email = email
        self.company = company
        self.phone = phone
        self.password = password
 

@app.route('/registration_landing')
def registration_landing():

    return render_template('registration_landing.html')

@app.route('/login/')
def login():

    if 'candidate' in session:
        return redirect(url_for('information'))
    elif 'employer' in session:
        return redirect(url_for('work_information'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():

    session.pop('candidate', None)
    session.pop('employer', None)

    session.clear()

    flash("You have been successfully logged out", "success")
    
    return redirect(url_for('login'))

@app.route('/', methods=['POST'])
def change():
    
        return render_template('index.html', user=session)

@app.route('/')
def index():

    #for token in doc:
      #  print(token.text)

    return render_template('index.html', user=session)

@app.route('/search')
def search():

    return render_template('search.html', user=session)

@app.route('/employers')
def employers():
    
    
    return render_template('employers.html', user=session)

@app.route('/choice')
def choice():

    return render_template('choice.html', user=session)

@app.route('/contact')
def contact():

    return render_template('contact.html', user=session)
@app.route('/employer_registration/')
def employer_registration():
    
    return render_template('employer_registration.html')

@app.route('/candidate_registration/')
def candidate_registration():
    
    return render_template('candidate_registration.html')

@app.route('/email_request/')
def email_request():

    return render_template('email_request.html')

@app.route('/login_submit', methods=['GET', 'POST'])
def login_submit():

    if  request.method == 'POST':
            submitted_email = request.form['email']
            submitted_password = request.form['password']

            flag = 0

            try:
                    candidate = Candidates.query.filter_by(email=submitted_email).first()

                    password = candidate.password

                    first_name = candidate.firstname

                    last_name = candidate.lastname

                    profile = candidate.profile

                    email = candidate.email

                    phone = candidate.phone

                    if sha256_crypt.verify(submitted_password, password):
                        
                        session.pop('candidate', None)

                        session.pop('last', None)

                        session['candidate'] = first_name

                        session['last'] = last_name

                        session['profile'] = profile

                        session['email'] = email

                        session['phone'] = phone

                        return redirect(url_for('information'))
                    else:
                        flash("Invalid Password", "fail")
                        return redirect(url_for('login'))
            except:
                    flag = 1;

            try:
                   employer = Employers.query.filter_by(email=submitted_email).first() 

                   password = employer.password

                   company_name = employer.company

                   email = employer.email

                   phone = employer.phone
                   
                   profile = employer.profile

                   id = employer.employer_id

                   if sha256_crypt.verify(submitted_password, password):

                       session.pop('employer', None)

                       session['employer'] = company_name

                       session['email'] = email

                       session['phone'] = phone

                       session['profile'] = profile 

                       session['id'] = id

                       return redirect(url_for('work_information'))
                        
                   else:
                        flash("Invalid Password", "fail")
                        return redirect(url_for('login'))
            except:
                    flag = 1;

            if flag == 1:
                
                flash("User does not exist", "fail")
                return redirect(url_for('login'))

    return render_template('login.html')

def is_logged_in_candidate(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'candidate' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login as a candidate account', 'fail')
            return redirect(url_for('login'))
    return wrap

def is_logged_in_employer(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'employer' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login as an employer account', 'fail')
            return redirect(url_for('login'))
    return wrap

@app.route('/candidate_submit', methods=['GET', 'POST'])
def candidate_submit():

    if  request.method == 'POST':
            first_name = request.form['first']
            last_name = request.form['last']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            confirm = request.form['confirm']

            if password == confirm:
                stored_password = sha256_crypt.hash(str(password))

                data = Candidates(first_name, last_name, phone, email, stored_password)

                data.profile = "Testing"

                try:
                    db.session.add(data)
                    db.session.commit()
                   
                except:
                    flash("User Already Exists", "fail")
                    return redirect(url_for('candidate_registration'))

                flash("Thank you for registering", "success")
                return redirect(url_for('login'))
            else:
                flash("Error: Passwords don't match", "fail")
                return redirect(url_for('candidate_registration'))

@app.route('/candidate_result/')
@is_logged_in_employer
def candidate_result():

    employer = Employers.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    return render_template('candidate_result.html', user=session, image_file=image_file)


@app.route('/adverts/')
@is_logged_in_employer
def adverts():

    employer = Employers.query.filter_by(email=session["email"]).first()

    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    adverts = Adverts.query.filter_by(employer_id=employer.employer_id).all()

    return render_template('adverts.html', user=session, image_file=image_file, adverts=adverts)

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)

    image_fn = random_hex + f_ext

    picture_path = os.path.join(app.root_path, 'static/profile_pics', image_fn)

    form_picture.save(picture_path)

    return image_fn

def save_resume(form_resume):

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_resume.filename)

    resume_fn = random_hex + f_ext

    resume_path = os.path.join(app.root_path, 'static/resumes', resume_fn)

    form_resume.save(resume_path)

    return resume_fn

@app.route('/employer_settings/', methods=['GET', 'POST'])
@is_logged_in_employer
def employer_settings():

    employer = Employers.query.filter_by(email=session["email"]).first()

    form = ImageForm()

    if form.validate_on_submit():
       if form.picture.data:

          picture_file = save_picture(form.picture.data)
            
          employer = Employers.query.filter_by(email=session["email"]).first()

          employer.image_file = picture_file

          db.session.commit()

          session.pop("picture", None)

          session["picture"] = picture_file

          flash("Picture Updated", "success")
          return redirect(url_for('employer_settings'))
    
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)
    return render_template('employer_settings.html', user=session, form=form, image_file=image_file)

@app.route('/upload_password/', methods=['GET', 'POST'])
def upload_password():

    if request.method == 'POST':

        try:

            candidate = Candidates.query.filter_by(email=session['email']).first()

            password = request.form['password']

            candidate.password = sha256_crypt.encrypt(str(password))

            db.session.commit()

            flash("Successfully changed password", "success")
            return redirect(url_for('candidate_settings'))

        except:
            
            pass

        try:

            employer = Employers.query.filter_by(email=session['email']).first()

            password = request.form['password']

            employer.password = sha256_crypt.encrypt(str(password))

            db.session.commit()

            flash("Successfully changed password", "success")
            return redirect(url_for('employer_settings'))

        except:

            pass

    return render_template('login.html')

@app.route('/upload_description/', methods=['GET', 'POST'])
def upload_description():

    if request.method == 'POST':

        try:

            candidate = Candidates.query.filter_by(email=session['email']).first()

            new_description = request.form['description']

            candidate.profile = new_description

            db.session.commit()

            session.pop('profile', None)

            session['profile'] = new_description 

            flash("Successfully saved your job description", "success")
            return redirect(url_for('candidate_settings'))

        except:
            
            pass

        try:

            employer = Employers.query.filter_by(email=session['email']).first()

            new_description = request.form['description']

            employer.profile = new_description

            db.session.commit()

            session['profile'] = new_description 

            flash("Successfully saved your job description", "success")
            return redirect(url_for('employer_settings'))

        except:

            pass

    return render_template('login.html')

@app.route('/post_job/', methods=['GET', 'POST'])
@is_logged_in_employer
def post_job():

    employer = Employers.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    form = InterviewForm()

    if form.validate_on_submit():

        salary = request.form['salary']
        position = request.form['position']
        experience = request.form['experience']
        candidatesNumber = request.form['candidatesNumber']
        description = request.form['description']
        interview_date = form.entryDate.data
        interview_time = form.entryTime.data
        location = request.form['location']

        job = position.lower()
        
        employer = Employers.query.filter_by(email=session['email']).first()

        id = int(employer.employer_id)       

        advert = Adverts(salary, job, experience, location, description, candidatesNumber, interview_date, interview_time, id)

        db.session.add(advert)

        db.session.commit()

        experience_years = str(experience) + " years"

        text_to_be_analyzed = str(position) + " " + experience_years + " " + str(description)

        job = Jobs(text_to_be_analyzed)

        db.session.add(job)

        db.session.commit()

        flash("Advert successfully added to your current adverts", "success")
        return redirect(url_for('post_job'))

    return render_template('post_job.html', user=session, image_file=image_file, form=form)

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():

    if request.method == 'POST' or request.method == 'GET':
       
       try:

            location_query = request.form['category']

       except: 
           flash("Please select a location", "result_feedback")
           return redirect(url_for('search'))

       try: 
           query = request.form['search_query']
           if query == "Search Job Position":
                query = None
           
       except:
           query = None

       if location_query == "Any" and query == None:

           adverts = Adverts.query.all()
           
       elif location_query == "Any" and query != None:

           print("here")
           adverts = Adverts.query.filter(Adverts.position.contains(query)).all()
       
       elif location_query != "Any" and query == None:

           adverts = Adverts.query.filter_by(location=location_query).all()

       elif location_query != "Any" and query != None:
           
           adverts = Adverts.query.filter(Adverts.location.contains(location_query), Adverts.position.contains(query)).all()
      
       employers = []

       if not adverts:
           flash("No results found", "result_feedback")
           return redirect(url_for('search'))
       else:

           image_dictionary = {}

           image_dictionary.clear()
            
           for advert in adverts:

               employer = Employers.query.filter_by(employer_id=advert.employer_id).first()

               image_dictionary[advert.employer_id] = employer.image_file

           return render_template('search_results.html', user=session, adverts=adverts, employers=employers, images=image_dictionary)

   
@app.route('/job_apply', methods=['GET', 'POST'])
@is_logged_in_candidate
def job_apply():

    id = request.form['advert_id']

    advert = Adverts.query.filter_by(advert_id=id).first()

    employer = Employers.query.filter_by(employer_id=advert.employer_id).first()

    image_file = employer.image_file

    return render_template('job_apply.html', user=session, advert=advert, employer=employer, image_file=image_file)

@app.route('/candidate_settings/', methods=['GET', 'POST'])
@is_logged_in_candidate
def candidate_settings():

    candidate = Candidates.query.filter_by(email=session["email"]).first()

    form = ImageForm()

    resumeForm = ResumeForm()

    if form.validate_on_submit():
       if form.picture.data:

          picture_file = save_picture(form.picture.data)
            
          candidate = Candidates.query.filter_by(email=session["email"]).first()

          candidate.image_file = picture_file

          db.session.commit()

          flash('Picture updated', 'success')
          return redirect(url_for('candidate_settings'))

    if resumeForm.validate_on_submit():
       if resumeForm.resume.data:

          resume_file = save_resume(resumeForm.resume.data)
            
          candidate = Candidates.query.filter_by(email=session["email"]).first()

          candidate.resume = resume_file

          db.session.commit()

          flash('Resume updated', 'success')

          return redirect(url_for('candidate_settings'))
   
    image_file = url_for('static', filename='profile_pics/' + candidate.image_file)

    return render_template('candidate_settings.html', user=session, form=form, resumeForm=resumeForm, image_file=image_file)

@app.route('/upload_resume/', methods=['GET', 'POST'])
@is_logged_in_candidate
def upload_resume():

    form = ResumeForm()

    if form.validate_on_submit():
       if form.resume.data:

          resume_file = save_resume(form.resume.data)
            
          candidate = Candidates.query.filter_by(email=session["email"]).first()

          candidate.resume_file = resume_file

          db.session.commit()

          flash('Resume updated', 'success')
          return redirect(url_for('candidate_settings'))
   

@app.route('/submissions/')
@is_logged_in_candidate
def submissions():

    candidate = Candidates.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + candidate.image_file)

    return render_template('submissions.html', user=session, image_file=image_file)

@app.route('/employer_information', methods=["POST", "GET"])
@is_logged_in_candidate
def employer_information():

    if request.method == "POST":

        id = request.form["advert_id"]

        advert = Adverts.query.filter_by(advert_id=id).first()
        
        employer = Employers.query.filter_by(employer_id=advert.employer_id).first()

        image_file = employer.image_file

        return render_template('employer_information.html', user=session, advert=advert, employer=employer, image_file=image_file)

@app.route('/candidate_apply', methods=["POST", "GET"])
@is_logged_in_candidate
def candidate_apply():

    if request.method == 'POST':

        advert_id = request.form["advert_id"]

        candidate = Candidates.query.filter_by(email=session["email"]).first()

        job = Jobs.query.filter_by(job_id=advert_id)

        if(candidate.resume == None):
            flash("Please upload your resume", "result_feedback")
            return redirect(url_for('search'))

        #submission = Submission()

        flash("You have successfully applied", "result_feedback")
        return redirect(url_for('search'))

    else:
        return redirect(url_for('search'))

@app.route('/employer_submit', methods=['GET', 'POST'])
def employer_submit():

    if  request.method == 'POST':
    
            email = request.form['email']
            company = request.form['company']
            phone = request.form['phone']
            password = request.form['password']
            confirm = request.form['confirm']

            format_company = company.upper()

            if password == confirm:
                stored_password = sha256_crypt.encrypt(str(password))

                data = Employers(email, format_company, phone, stored_password)

                try:
                    db.session.add(data)
                    db.session.commit()
                   
                except:
                    flash("Employer Already Exists", "fail")
                    return redirect(url_for('employer_registration'))

                flash("Thank you for registering", "success")
                return redirect(url_for('login'))
            else:
                flash("Error: Passwords don't match", "fail")
                return redirect(url_for('employer_registration'))

@app.route('/password_request/', methods=['GET', 'POST'])
def password_submit():

    if  request.method == 'POST':
            email = request.form['email']
            
            if password == confirm:
                stored_password = sha256_crypt.encrypt(str(password))
                flash("Thank you for registering", "success")
                return redirect(url_for('login'))
            else:
                flash("Error: Passwords don't match", "fail")
                return redirect(url_for('candidate_registration'))

@app.route('/information/')
@is_logged_in_candidate
def information():

   candidate = Candidates.query.filter_by(email=session["email"]).first()
   image_file = url_for('static', filename='profile_pics/' + candidate.image_file)

   if candidate.resume != None:

        resume_file = url_for('static', filename='resumes/' + candidate.resume)
        return render_template('information.html', user=session, image_file=image_file, resume_file=resume_file)
   else: 
        return render_template('information.html', user=session, image_file=image_file)

@app.route('/work_information/')
@is_logged_in_employer
def work_information():
    employer = Employers.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    return render_template('work_information.html', user=session, image_file = image_file)

if __name__ == '__main__':

    app.secret_key = 'super secret key'
    app.run()

    