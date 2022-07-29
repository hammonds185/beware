from flask import Flask, render_template, abort, request, flash
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

def configure():
    load_dotenv()

@app.route("/")
def home():
    return render_template('home.html')  

@app.route("/bewaremap")
def first_map():
    # default map is NY
    return render_template('bewaremap.html', latitude = 40.7128, longitude = 74.0060, url = "https://maps.googleapis.com/maps/api/js?key=" + os.getenv('API_KEY') + "&callback=initMap")

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
        LAT = location['lat']
        LNG = location['lng']
    else:
        return "address is invalid"
    return render_template('bewaremap.html', latitude = LAT, longitude = LNG, url = "https://maps.googleapis.com/maps/api/js?key=" + os.getenv('API_KEY') + "&callback=initMap") 

@app.route("/login")
def login():
    return render_template('login.html') 

@app.route("/myprofile")
def profile():
    return render_template('profile.html') 

@app.route("/report")
def report():
    return render_template('report.html')

if __name__ == '__main__': 
    configure()
    app.run(debug=True, host="0.0.0.0")
