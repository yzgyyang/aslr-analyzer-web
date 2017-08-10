from flask import Flask, render_template, request, url_for

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result')
@app.route('/result/<os_name>')
def results(os_name="freebsd"):
    return render_template("result.html", os_name=os_name)
