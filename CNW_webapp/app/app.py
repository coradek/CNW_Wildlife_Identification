from flask import Flask, render_template, request
app = Flask(__name__)


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



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=False)
