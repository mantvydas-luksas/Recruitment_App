from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Text
from sqlalchemy.orm import relationship 
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
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

TRAIN_DATA = [
("Dynamic individual with 6 years of software development experience in design, development, deployment, maintenance, production and support of web - based and Client-Server business applications using OOP and Java/J2EE technologies. ",{"entities":[(0,60,"years")]})
]

ner.add_label('skills')

pipe_exceptions = ["ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

with nlp.disable_pipes(*unaffected_pipes):
    for iteration in range(20):
        random.shuffle(TRAIN_DATA)
        for raw_text,entity_offsets in TRAIN_DATA:
            doc=nlp.make_doc(raw_text)
            nlp.update([Example.from_dict(doc,entity_offsets)])

doc = nlp("Dynamic individual with 6 years of software development experience in design, development, deployment, maintenance, production and support of web - based and Client-Server business ")

#for ent in doc.ents:
   #print(ent.label_, ent.text)

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

class Candidates(db.Model):
    __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    profile = db.Column(db.Text)
    resume = db.Column(db.Text)
    
    
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
  
    def __init__(self, result, resume_entities):
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
    skills = db.Column(db.Text)
    position = db.Column(db.String(255))
    description = db.Column(db.Text)
    experience = db.Column(db.Integer)
    employer_id = db.Column(db.Integer, ForeignKey("employers.employer_id"))
   
    def __init__(self, skills, position, description, experience):
        self.skills = skills
        self.position = position
        self.description = description
        self.experience = experience

class Employers(db.Model):
    __tablename__ = 'employers'
    employer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    company = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255))
    profile = db.Column(db.Text)
    
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

                   if sha256_crypt.verify(submitted_password, password):

                       session.pop('employer', None)

                       session['employer'] = company_name

                       session['email'] = email

                       session['phone'] = phone

                       return redirect(url_for('work_information'))
                        
                   else:
                        flash("Invalid Password", "fail")
                        return redirect(url_for('login'))
            except:
                    flag = 1;

            if flag == 1:
                
                flash("User does not exist", "fail")
                return redirect(url_for('login'))

def is_logged_in_candidate(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'candidate' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized Access, Please Login', 'fail')
            return redirect(url_for('login'))
    return wrap

def is_logged_in_employer(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'employer' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized Access, Please Login', 'fail')
            return redirect(url_for('login'))
    return wrap



@app.route('/candidate_submit/', methods=['GET', 'POST'])
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

@app.route('/employer_upload/', methods=['GET', 'POST'])
@is_logged_in_employer
def upload_employer_picture():

   try:
       employer = Employers.query.filter_by(email=session['email']).first()

       employer.profile = 'Hello'

       db.sessions.commit()
   
   except:

        return redirect(url_for('search'))

@app.route('/candidate_upload/', methods=['GET', 'POST'])
@is_logged_in_candidate
def upload_candidate_profile():

   try:
       candidate = Candidates.query.filter_by(email=session['email']).first()

       candidate.profile = 'Hello'

       db.sessions.commit()
   
   except:

        return redirect(url_for('search'))

@app.route('/candidate_result/')
@is_logged_in_employer
def candidate_result():

    return render_template('candidate_result.html', user=session)


@app.route('/adverts/')
@is_logged_in_employer
def adverts():

    return render_template('adverts.html', user=session)


@app.route('/employer_settings/')
@is_logged_in_employer
def employer_settings():

    return render_template('employer_settings.html', user=session)

@app.route('/post_job/')
@is_logged_in_employer
def post_job():

    return render_template('post_job.html', user=session)

@app.route('/candidate_settings/')
@is_logged_in_candidate
def candidate_settings():

    return render_template('candidate_settings.html', user=session)

@app.route('/submissions/')
@is_logged_in_candidate
def submissions():

    return render_template('submissions.html', user=session)

@app.route('/employer_submit/', methods=['GET', 'POST'])
def employer_submit():

    if  request.method == 'POST':
    
            email = request.form['email']
            company = request.form['company']
            phone = request.form['phone']
            password = request.form['password']
            confirm = request.form['confirm']

            if password == confirm:
                stored_password = sha256_crypt.encrypt(str(password))

                data = Employers(email, company, phone, stored_password)

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

   return render_template('information.html', user=session)
    
@app.route('/work_information/')
@is_logged_in_employer
def work_information():

    return render_template('work_information.html', user=session)

if __name__ == '__main__':

    app.secret_key = 'super secret key'
    app.run()

    