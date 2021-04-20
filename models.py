from sqlalchemy import Integer, ForeignKey, String, Column, Text
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence

Base = declarative_base()

class Candidates(Base):
    __tablename__ = 'candidates'
    candidate_id = Column(Integer, primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    profile = Column(Text, nullable=False, default='No profile description added yet.')
    resume = Column(String(20))
    image_file = Column(String(20), nullable=False, default='profile_default.png')
    confirm_email = Column(Boolean, default=False)

    submissions = relationship("Submissions", backref="candidates",  cascade="all, delete-orphan")

    def __init__(self, firstname, lastname, phone, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.password = password

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.candidate_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        
        s = Serializer(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return Candidates.query.get(user_id)

class Submissions(Base):
    __tablename__ = 'submissions'
    submission_id = Column(Integer, primary_key=True)
    result = Column(Integer)
    resume_entities= Column(Text)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete='CASCADE'))
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete='CASCADE'))
    employer_id = Column(Integer, ForeignKey("employers.employer_id", ondelete='CASCADE'))
  
    def __init__(self, resume_entities, candidate_id, job_id, employer_id):
        self.result = result
        self.resume_entities = resume_entities
     
class Jobs(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True)
    description_entities= Column(Text)

    submissions = relationship("Submissions", backref="jobs",  cascade="all, delete-orphan")

    def __init__(self, description_entities):
        self.description_entities = description_entities

class Adverts(Base):
    __tablename__ = 'adverts'
    advert_id = Column(Integer, primary_key=True)
    salary = Column(Integer)
    position = Column(String(255))
    experience = Column(Integer)
    location = Column(String(255))
    description = Column(Text)
    candidates_number = Column(Integer)
    date = Column(Text)
    time = Column(Text)
    employer_id = Column(Integer, ForeignKey("employers.employer_id", ondelete='CASCADE'))
    

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

class Employers(Base):
    __tablename__ = 'employers'
    employer_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    company = Column(String(255))
    phone = Column(String(255))
    password = Column(String(255))
    profile = Column(Text, nullable=False, default='No profile description added yet.')
    image_file = Column(String(20), nullable=False, default='profile_default.png')
    confirm_email = Column(Boolean, default=False)

    submissions = relationship("Submissions", backref="employers",  cascade="all, delete-orphan")
    adverts = relationship("Adverts", backref="employers",  cascade="all, delete-orphan")

    def __init__(self, email, company, phone, password):
        self.email = email
        self.company = company
        self.phone = phone
        self.password = password

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.employer_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        
        s = Serializer(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return Employers.query.get(user_id)
 
