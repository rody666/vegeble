from flask import Flask, request, render_template
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/name', methods=['POST'])
def name():
    name = request.form['username']
    return f'your name is {name}'

@app.route('/result',methods=['POST'])
def result():
    value1 = int(request.form['value1'])
    value2 = int(request.form['value2'])
    output1 = f'{value1}+{value2}={value1+value2}'
    output2 = f'{value1}*{value2}={value1*value2}'
    return output1 +"<br>"+ output2

@app.route('/omikuji', methods=['POST'])
def omikuji():
    num = randint(1,10)
    if num == 1:
        result = '大吉!!!!'
    elif 2<=num<=4:
        result = '中吉!!'
    elif 5<=num<=8:
        result = '小吉'
    else:
        result = '凶'
    return render_template('result3.html',result = result)

@app.route('/check',methods=['POST'])
def check():
    num = int(request.form['num'])
    if num % 2 == 0:
        return f'{num} is Even number'
    else:
        return f'{num} is Odd number'

if __name__ == '__main__':
    app.run(debug=True)