from flask import Flask, render_template, abort, request, flash
from dotenv import load_dotenv
import os

app = Flask(__name__)

def configure():
    load_dotenv()

@app.route("/")
def home():
    return render_template('home.html') 

@app.route("/crimemap")
def crime_map():
    return render_template('crimemap.html', latitude = 0, longitude = 0, url = "https://maps.googleapis.com/maps/api/js?key=" + os.getenv('API_KEY') + "&callback=initMap") 

@app.route("/bewaremap")
def beware_map():
    return render_template('bewaremap.html', latitude = 0, longitude = 0, url = "https://maps.googleapis.com/maps/api/js?key=" + os.getenv('API_KEY') + "&callback=initMap") 

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
