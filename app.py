from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import os
from prediction import *

UPLOAD_FOLDER = 'static\\'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Upload', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return render_template("index.html")
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return render_template("index.html")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("response.html",data=Predict(filename),path=filename)
            return render_template("index.html")
    except:
        return render_template("index.html")    


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')        
