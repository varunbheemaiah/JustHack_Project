#Imports
#------------------------------------------------------------------------------#

import os
from flask import Flask, render_template, request, redirect, session, flash
import urllib.request
from flask import send_file
import sqlite3
from flask import g
import hashlib

#------------------------------------------------------------------------------#

#Initial Setups
#------------------------------------------------------------------------------#

salt = "TwinFuries"
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = os.urandom(24)

#------------------------------------------------------------------------------#

#Database Setup and functions
#------------------------------------------------------------------------------#

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

#------------------------------------------------------------------------------#

#Website routes
#------------------------------------------------------------------------------#

#Login Page(Everyone)
#------------------------------------------------------------------------------#

@app.route('/', methods = ['POST' , 'GET'])
def index():
    message = ""
    if request.method == 'POST':
        user = request.form['username']
        pswdun = request.form['password']+salt
        pswd = hashlib.md5(pswdun.encode())
        password = query_db('select password from Details where Username="'+user+'"')
        if password:
            if password[0][0] == pswd.hexdigest():
                session['user'] = user
                return redirect('/home')
        else:
            message = "Invalid Username or Password"
    return render_template('login.html', confirm = message)

#------------------------------------------------------------------------------#

#Registration Page(Everyone)
#------------------------------------------------------------------------------#

@app.route('/register', methods = ['GET', 'POST'])
def register():
    failed = ""
    if request.method == 'POST':
        username = request.form['username']
        college = request.form['college']
        email = request.form['email']
        passwordun = request.form['pwd1']+salt
        password = hashlib.md5(passwordun.encode())
        chkmail = query_db('select Username from Details where Email="'+email+'"')
        if chkmail:
            failed = "Email already registered"
        else:
            execute_db('insert into Details values("'+username+'","'+email+'","'+college+'","'+password.hexdigest()+'")')
            return redirect('/')
    return render_template('register.html', message = failed)

#------------------------------------------------------------------------------#

@app.route('/db_add')
def adddata():
    pass

#Home Page(Logged in)
#------------------------------------------------------------------------------#

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    flash("Log in to view this page")
    return redirect('/')

#------------------------------------------------------------------------------#

#Upload file(Logged in)
#------------------------------------------------------------------------------#

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    message = ""
    if 'user' in session:
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
    flash("Log in to view this page")
    return redirect('/')

#------------------------------------------------------------------------------#

#Upload link(Logged in)
#------------------------------------------------------------------------------#

@app.route('/link', methods = ['GET', 'POST'])
def download_link():
    if 'user' in session:
        if request.method == 'POST':
                target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
                url = request.form['link']
                fname = url[url.rfind("/")+1:]
                destination = "/".join([target,fname])
                urllib.request.urlretrieve("http://"+url,destination)
                message = "File will be added if available"
        return render_template('linksend.html',confirm = message)
    flash("Log in to view this page")
    return redirect('/')

#------------------------------------------------------------------------------#

#Download Uploaded_Notes(Logged in)
#------------------------------------------------------------------------------#

@app.route('/download')
def download():
    if 'user' in session:
        file_list = []
        target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
        for root, dirs, files in os.walk(target):
            for filename in files:
                file_list.append(filename)
        return render_template('download.html', fnames = file_list)
    flash("Log in to view this page")
    return redirect('/')

@app.route('/download/<fname>', methods = ['GET' , 'POST'])
def download_file(fname):
    if 'user' in session:
        target = os.path.join(APP_ROOT, 'Uploaded_Notes/')
        destination = "/".join([target,fname])
        return send_file(destination, as_attachment=True)
    flash("Log in to view this page")
    return redirect('/')

#------------------------------------------------------------------------------#

#uploadoptions(Logged in)
#------------------------------------------------------------------------------#

@app.route('/uploadoptions')
def downloadoptions():
    if 'user' in session:
        return render_template('downloadoptions.html')
    flash("Log in to view this page")
    return redirect('/')

#Logout
#------------------------------------------------------------------------------#

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#


if __name__ == '__main__':
   app.run(debug = True)
