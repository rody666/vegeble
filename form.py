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

@app.route('/calculate',methods=['POST'])
def calc():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    ope = request.form['operator']
    if ope == 'sum':
        return f'{num1}+{num2}={num1+num2}'
    elif ope == 'dif':
        return f'{num1}-{num2}={num1-num2}'
    elif ope == 'pro':
        return f'{num1}*{num2}={num1*num2}'
    elif ope == 'quo':
        return f'{num1}/{num2}={num1/num2}'
        
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