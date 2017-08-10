from flask import Flask, render_template, request, url_for

# Initialize the Flask application
app = Flask(__name__)

# Constants
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
    return render_template("index.html")

@app.route('/results')
@app.route('/results/<os_name>')
def results(os_name="freebsd"):
    return render_template("result.html",
        os_name=os_name, tested_os=TESTED_OS)
