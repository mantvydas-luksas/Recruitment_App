from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import spacy
import json
import random
import en

from spacy.tokens import Doc
from spacy.training import Example

from spacy.util import minibatch, compounding
from pathlib import Path

nlp = en.load()


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

for ent in doc.ents:
   print(ent.label_, ent.text)

ENV = 'prod'
   
app= Flask(__name__)

if ENV == 'dev':
     app.debug = True
     app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
     app.debug = False
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kdtfxcdxnpszrq:c8dccd8f82d7b2f33d7da031caaf9e791ded57472c9ef082c7870b5527cc7a6e@ec2-34-252-251-16.eu-west-1.compute.amazonaws.com:5432/da7ukihqat8bgm'

@app.route('/', methods=['POST'])
def redirect():
    
        return render_template('index.html')

@app.route('/')
def index():

    for token in doc:
        print(token.text)

    return render_template('index.html')

@app.route('/search')
def search():

    return render_template('search.html')

@app.route('/employers')
def employers():
    
    return render_template('employers.html')

if __name__ == '__main__':
   
    app.run()

    