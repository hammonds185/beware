from flask import Flask, render_template, redirect, url_for, abort, request, flash, session, jsonify
from flask_session import Session
from dotenv import load_dotenv
from __init__ import app, db, bcrypt
from forms import *
from model import *
import requests
import os
from datetime import datetime
import json
from werkzeug.utils import secure_filename
from uuid import uuid4

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
API_KEY = os.getenv('API_KEY')
if API_KEY == None:
    API_KEY = ""
autocomplete_src = "https://maps.googleapis.com/maps/api/js?key=" + API_KEY + "&libraries=places&callback=initAutocomplete"
map_src = "https://maps.googleapis.com/maps/api/js?key=" + API_KEY + "&callback=initMap"
types = {"robbery":"Robbery/Theft","burglary":"Burglary", "police": "Missing Person",
        "discrimination":"Hate Crime","racial_profiling":"Racial Profiling", "customer_service":"Bad Customer Service",
        "car_accident":"Car Accident", "assault":"Assault", "other":"Other" }


#Default LAT and LNG is NY
LNG = -74.0060
LAT = 40.7128

def configure():
    load_dotenv()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/bewaremap")
def first_map():
    return render_template('location.html', autocomplete_src = autocomplete_src, values = Report.query.all())

@app.route("/bewaremap", methods=['POST', 'GET'])
def beware_map():
    address = request.form["location"]
    params = {
        'key': os.getenv('API_KEY'),
        'address': address
    }
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        global LAT 
        LAT = location['lat']
        global LNG 
        LNG = location['lng']
    else:
        return "address is invalid"
    return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.all()) 

@app.route("/bewaremaplight")
def beware_map_light():
    return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.all()) 


@app.route("/bewaremapdark")
def beware_map_dark():
    return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.all()) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        email=form.email.data
        password=form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #flash(f'Logging you in', 'success')
            session['username'] = user.username
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username', None)
    return redirect(url_for('home'))

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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/myprofile")
def profile():
    if session.get('username'):
        return render_template('profile.html', user_reports= Report.query.filter_by(username=session['username']).all(), username= session['username'], types = types) 
    else:
        return redirect(url_for('home'))

def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"

@app.route("/report", methods=['POST', 'GET'])
def report(): 
    if session.get('username'):   
        if request.method == "POST":
            # get info from form
            where = request.form.get("where")
            thetype = request.form.get("type")
            date = request.form.get("date")
            description = request.form.get("description")
            # make datetime object
            dto = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            print("date:" + str(dto))
            # get Lat and long
            params = {
                'key': os.getenv('API_KEY'),
                'address': where
            }
            base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            response = requests.get(base_url, params=params)
            data = response.json()
            if data['status'] == 'OK':
                result = data['results'][0]
                location = result['geometry']['location']
                lat = location['lat']
                lng = location['lng']
                filename = None
                # image file
                if 'file' in request.files:
                    file = request.files['file']
                    if file.filename == '':
                        # flash('No selected file')
                        print("no file selected")
                    else:
                        print("new file name")
                        original_filename = secure_filename(file.filename)
                        filename = make_unique(original_filename)
                        file.save(os.path.join(app.root_path,app.config['UPLOAD_FOLDER'], filename))

                # create report for database
                report = Report(address = where, incident = thetype, date = dto, description = description, latitude = lat, longitude = lng, username = session['username'],image_file=filename)
            else:
                # will make do something else
                return "address is invalid"
                
            #### for me and my confirmation only ####
            print(request.form.get("where"))
            print(request.form.get("type"))
            print(request.form.get("date"))
            print(request.form.get("description"))
            #### end for me and my confirmation only. ####
            # add and commit ot database
            db.session.add(report)
            db.session.commit()
            #### for me and my confirmation only ####
            print(report)
            print(Report.query.all())
            #### end for me and my confirmation only. ####
            # open profile page when successful
            return render_template('profile.html', user_reports= Report.query.filter_by(username=session['username']).all(), username= session['username'],types = types)
        return render_template('report.html', autocomplete_src = autocomplete_src, values = Report.query.all())
    else:
        return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Report.query.get(noteId)
    print("hey")
    if note: 
        db.session.delete(note)
        db.session.commit()
    return jsonify({})


# Buttons Redirect 
@app.route("/show_all")
def show_all():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.all()) 
@app.route("/robbery")
def robbery():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='robbery').all()) 
@app.route("/burglary")
def burglary():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='burglary').all()) 
@app.route("/assault")
def assault():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='assault').all()) 
@app.route("/hate_crime")
def hate_crime():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='discrimination').all()) 
@app.route("/racial_profiling")
def racial_profiling():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='racial_profiling').all()) 
@app.route("/bad_customer_service")
def bad_customer_service():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='customer_service').all()) 
@app.route("/car_accident")
def car_accident():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='car_accident').all()) 
@app.route("/missing_person")
def missing_person():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='police').all()) 
@app.route("/other")
def other():
     return render_template('bewaremap.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='other').all()) 


# Buttons Dark mode
@app.route("/show_all_dark")
def show_all_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.all()) 
@app.route("/robbery_dark")
def robbery_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='robbery').all()) 
@app.route("/burglary_dark")
def burglary_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='burglary').all()) 
@app.route("/assault_dark")
def assault_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='assault').all()) 
@app.route("/hate_crime_dark")
def hate_crime_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='discrimination').all()) 
@app.route("/racial_profiling_dark")
def racial_profiling_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='racial_profiling').all()) 
@app.route("/bad_customer_service_dark")
def bad_customer_service_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='customer_service').all()) 
@app.route("/car_accident_dark")
def car_accident_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='car_accident').all()) 
@app.route("/missing_person_dark")
def missing_person_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='police').all()) 
@app.route("/other_dark")
def other_dark():
     return render_template('bewaremapdark.html', latitude = LAT, longitude = LNG, map_src = map_src, values = Report.query.filter_by(incident='other').all()) 


if __name__ == '__main__': 
    configure()
    app.run(debug=True, host="0.0.0.0")
