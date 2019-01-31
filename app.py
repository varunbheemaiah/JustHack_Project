import os
from flask import Flask, render_template, request
import urllib.request
from flask import send_file

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
        destination = "/".join([target,fname])
        if(os.path.isfile(destination)):
            message = "We already have those notes"
        else:
            f.save(destination)
            message = "File Uploaded Successfully"
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

if __name__ == '__main__':
   app.run(debug = True)
