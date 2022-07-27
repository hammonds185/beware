from flask import Flask, render_template, abort, request, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html') 

if __name__ == '__main__':
    # configure()
    app.run(debug=True, host="0.0.0.0")