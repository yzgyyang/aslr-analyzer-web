from flask import Flask, render_template, request, url_for

# Initialize the Flask application
app = Flask(__name__)

# Constants
NAVS = [
    ('index', 'Home'),
    ('new', 'New'),
    ('results', 'Results')
]

TESTED_OS = [
    ('freebsd', 'FreeBSD 12-CURRENT with ASLR Patch'),
    ('openbsd', 'OpenBSD 6.1'),
    ('netbsd', 'NetBSD 7.1'),
    ('dragonfly', 'DragonFly BSD 4.8.1'),
    ('macos', 'macOS 10.12'),
    ('ubuntu', 'Ubuntu 17.04'),
    ('arch', 'Arch Linux 201708')
]

@app.route('/')
def index():
    return render_template("index.html",
        nav_name="index",
        navs=NAVS)

@app.route('/new')
def new():
    pass

@app.route('/results')
@app.route('/results/<os_name>')
def results(os_name="freebsd"):
    return render_template("result.html",
        os_name=os_name,
        tested_os=TESTED_OS,
        navs=NAVS)
