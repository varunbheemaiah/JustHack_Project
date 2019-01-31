import os
from flask import Flask, render_template, request, redirect
import urllib.request
from flask import send_file
import sqlite3
from flask import g

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(APP_ROOT,'Database/database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        #db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.route('/init_db')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query):
    cur = get_db()
    cur.execute(query)
    cur.commit()
    cur.close()

@app.route('/', methods = ['POST' , 'GET'])
def index():
    message = ""
    if request.method == 'POST':
        user = request.form['username']
        pswd = request.form['password']
        password = query_db('select password from Details where Username="'+user+'"')
        if password:
            if password[0][0] == pswd:
                return redirect('/home')
        else:
            message = "Invalid Username or Password"
    return render_template('login.html', confirm = message)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        college = request.form['college']
        email = request.form['email']
        password = request.form['pwd1']
        execute_db('insert into Details values("'+username+'","'+email+'","'+college+'","'+password+'")')
        return redirect('/home')
    return render_template('register.html')

@app.route('/db_add')
def adddata():
    pass



@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
        if not os.path.isdir(target):
            os.mkdir(target)
        f = request.files['file']
        fname = f.filename
        filenamels = fname.split(".")
        validfiles = ["doc" , "docx" , "pdf", "epub"]
        if filenamels[1] in validfiles:
            destination = "/".join([target,fname])
            if(os.path.isfile(destination)):
                message = "We already have those notes"
            else:
                f.save(destination)
                message = "File Uploaded Successfully"
        else:
            message = "Invalid File Format"
    return render_template('upload.html',confirm = message)

@app.route('/link')
def link():
    return render_template('linksend.html')

@app.route('/linksend', methods = ['GET', 'POST'])
def download_link():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
        url = request.form['link']
        fname = url[url.rfind("/")+1:]
        destination = "/".join([target,fname])
        urllib.request.urlretrieve("http://"+url,destination)
        message = "File will be added if available"
    return render_template('linksend.html',confirm = message)

@app.route('/download')
def download():
    file_list = []
    target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
    for root, dirs, files in os.walk(target):
        for filename in files:
            file_list.append(filename)
    return render_template('download.html', fnames = file_list)

@app.route('/download/<fname>', methods = ['GET' , 'POST'])
def download_file(fname):
    target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
    destination = "/".join([target,fname])
    return send_file(destination, as_attachment=True)

@app.route('/downloadoptions')
def downloadoptions():
    return render_template('downloadoptions.html')


if __name__ == '__main__':
   app.run(debug = True)
