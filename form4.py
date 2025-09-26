from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form4.html')

@app.route('/check',methods=['POST'])
def check():
    num = int(request.form['num'])
    if num % 2 == 0:
        return f'{num} is Even number'
    else:
        return f'{num} is Odd number'

if __name__ == '__main__':
    app.run(debug=True)