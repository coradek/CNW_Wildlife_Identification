from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'app/tmp/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'JPG'])


# home page
@app.route('/')
def index():
    # return render_template('my_index.html')
    return render_template('index.html')

# Submit page
@app.route('/submit')
def submit():
    return render_template('submit.html')


# Predict page
@app.route('/predict', methods = ['POST'])
def predict():

    doc = str(request.form['user_input'])

    X = vectorizer.transform([doc])
    pred = model.predict(X)
    return render_template('predict.html', result = pred[0])


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('tmp/'+secure_filename(f.filename))
      return 'file uploaded successfully'



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
