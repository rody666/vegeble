from flask import Flask, request, render_template
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/name', methods=['POST'])
def name():
    name = request.form.get('username','guest')
    return f'your name is {name}'

@app.route('/calculate',methods=['POST'])
def calc():
    operations = {
        'sum':(lambda a,b: f'{a}+{b}={a+b}'),
        'dif':(lambda a,b: f'{a}-{b}={a-b}'),
        'pro':(lambda a,b: f'{a}*{b}={a*b}'),
        'quo':(lambda a,b: f'{a}/{b}={a/b}' if b != 0 else 'Error: Division by zero')
    }
    ope = request.form.get('operator','sum')
    try:
        num1,num2 = float(request.form['num1']),float(request.form['num2'])
    except ValueError:
        return '400: Bad Request<br>Enter number',400
    else:
        return operations[ope](num1,num2)

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
    return render_template('omikuji.html',result = result)

@app.route('/check',methods=['POST'])
def check():
    try:
        num = int(request.form['num'])
    except ValueError:
        return '400: Bad Request<br>Enter number',400
    else:
        return 'Even' if num%2 == 0 else 'Odd'
if __name__ == '__main__':
    app.run(debug=True)