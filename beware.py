from flask import Flask, render_template, abort, request, flash

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html') 

@app.route("/crimemap")
def crime_map():
    return render_template('crimemap.html') 

@app.route("/bewaremap")
def beware_map():
    return render_template('bewaremap.html') 

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
    # configure()
    app.run(debug=True, host="0.0.0.0")