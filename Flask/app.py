import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# Configs
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'out'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

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
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded', filename=filename))
    return '''
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/new/<filename>')
def uploaded(filename):
    return filename

@app.route('/results')
@app.route('/results/<os_name>')
def results(os_name="freebsd"):
    return render_template("result.html",
        os_name=os_name,
        tested_os=TESTED_OS,
        navs=NAVS)


# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
