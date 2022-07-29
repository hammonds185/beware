from flask import Flask, render_template, redirect, url_for, abort, request, flash, session
from dotenv import load_dotenv
from __init__ import app, db, bcrypt
from forms import *
from model import *
import os

def configure():
    load_dotenv()

@app.route("/")
def home():
    return render_template('home.html')  

@app.route("/bewaremap")
def beware_map():
    return render_template('bewaremap.html', latitude = 0, longitude = 0, url = "https://maps.googleapis.com/maps/api/js?key=" + os.getenv('API_KEY') + "&callback=initMap") 

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        email=form.email.data
        password=form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'Logging you in', 'success')
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global user
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")   
        user = User(username = form.username.data, email = form.email.data, password = pwd_hash)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('username or email taken, try again')
            return render_template('register.html', title='Register', form=form)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/myprofile")
def profile():
    return render_template('profile.html') 

@app.route("/report")
def report():
    return render_template('report.html')

if __name__ == '__main__': 
    configure()
    app.run(debug=True, host="0.0.0.0")
