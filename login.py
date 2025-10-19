from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('assenssment.html')

@app.route('/assenssment')
def assenssment():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)