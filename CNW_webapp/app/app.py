from flask import Flask, render_template, request
from werkzeug import secure_filename
import web_predictor as wp


app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'tmp/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'JPG'])


# home page
@app.route('/')
def index():
    return render_template('index.html')

# Submit page
@app.route('/submit')
def submit():
    return render_template('submit.html')


# Upload page
@app.route('/upload')
def upload():
    return render_template('upload.html')


# Process photo and show Result page
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        photo_name = 'tmp/'+secure_filename(f.filename)
        photo = 'app/static/'+photo_name
        f.save(photo)
        plot_name = photo_name[:-4]+'_plot'
        plot = 'app/static/'+plot_name
        print "\n plot will be saved to", plot

        result = wp.primary(photo, session, tensor, plot)

        return render_template('results.html', photo = photo_name,
                                plot = plot_name+'.png')

# set session and tensor globally to save overhead
session, tensor = wp.setup()
result = wp.primary('app/static/tmp/bunny.JPG', session, tensor, 'app/static/tmp/wptest')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8081, debug=True)
