from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from pymongo import MongoClient
import os, hashlib
import certifi
from datetime import datetime

now = datetime.now()

app = Flask(__name__)

app.secret_key = 'lovelovelovelovelovelovelovelo'

@app.route('/')
def home():
    all_db = db.write.find()
    if 'username' in session:
        username = session['username']
        return render_template('index.html', login=True, username=username, all_db=all_db)
    else: 
        return render_template('index.html', login=False)
    

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['_id']
        pwd = request.form['_pwd']
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/signup')
def signup():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', login=True, username=username)
    return render_template('signup.html')

@app.route('/write', methods=['GET','POST'])
def write():
    if request.method == 'POST':
        subject = request.form['_subject']
        desc = request.form['_desc']
        day = now.day
        
        doc = {
            'num' : db.testdbda.count_documents({}) + 1,
            'subject': subject,
            'desc' : desc,
            'name' : session['username'],
            'day' : day,
        }
        
        db.write.insert_one(doc)


        return redirect(url_for('home'))


@app.route('/signup_get', methods=['GET','POST'])
def signup_get():
    if request.method == 'POST':
        uid = request.form['_id']
        pwd = request.form['_pwd']
        name = request.form['_name']
        print(uid,pwd,name)

        doc = {
            'uid' : uid,
            'pwd' : hashlib.sha256(pwd.encode('utf-8')).hexdigest(),
            'name' : name,
        }

        db.user.insert_one(doc)
    
    return redirect(url_for('home'))


if __name__ == '__main__':
       app.run('0.0.0.0', port=80, debug=True)
