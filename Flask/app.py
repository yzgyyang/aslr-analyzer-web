import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.embed import components
from operator import itemgetter

import ast


# Reverse Proxy + Subfolder
# Solution from: https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes/36033627#36033627
class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


# Initialize the Flask application
app = Flask(__name__)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/aslr')

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
    ('arch', 'Arch Linux 201708')
]


@app.route('/')
def index():
    return render_template("index.html",
        nav_name="index",
        navs=NAVS)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == "POST":
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded', filename=filename))
    return '''
    <!doctype html>
    <form method=post enctype=multipart/form-data>
      git clone https://github.com/yzgyyang/getaddrs </br>
      cd getaddrs </br>
      [make, bmake] </br>
      ./getaddrs 100000 > output.txt </br>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/new/<filename>')
def uploaded(filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
        c = '[' + f.read() + ']'
        c = ast.literal_eval(c)
        # TYPE
        TYPE = 6
        c = [x[TYPE] for x in c]
        # Basic Statistics
        len_c = len(c)
        min_c = c[0]
        max_c = c[0]
        for x in c:
            if min_c > x:
                min_c = x
            if max_c < x:
                max_c = x
        range_c = (max_c - min_c)
        interval_c = int(range_c / 100)
        # Calc
        c2 = {}
        for x in c:
            try:
                c2[int(x / interval_c)] += 1
            except:
                c2[int(x / interval_c)] = 1
        c3 = []
        for key, value in c2.items():
            c3.append([key, value / len_c])
        c3 = sorted(c3, key=itemgetter(0))
        # Plot
        p = figure(title="Histogram (100 bins)", background_fill_color="#E8DDCB", plot_width=900, plot_height=600)
        p.line(np.linspace(0, 100, 100), 0.01, line_color="#F46D43", line_width=10, legend="Expected")
        p.line([x[0] for x in c3], [x[1] for x in c3], line_color="#036564", line_width=4, legend="Result")
        p.legend.location = "center_right"
        p.legend.background_fill_color = "darkgrey"
        p.xaxis.axis_label = 'bins'
        p.yaxis.axis_label = 'Probability'
        # Output
        script, div = components(p)
    return render_template("result_new.html",
        the_div=div,
        the_script=script)

@app.route('/results')
@app.route('/results/<os_name>')
def results(os_name="freebsd"):
    return render_template("result.html",
        os_name=os_name,
        tested_os=TESTED_OS,
        navs=NAVS)

@app.route('/results/<os_name>/<test_name>/<graph_name>')
def results_interactive(os_name, test_name, graph_name):
    return render_template("result_interactive.html",
        os_name=os_name,
        test_name=test_name,
        graph_name=graph_name,
        navs=NAVS)

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
