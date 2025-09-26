from flask import Flask, render_template
import random
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form3.html')

@app.route('/omikuji', methods=['POST'])
def omikuji():
    num = random.randint(1,10)
    if num == 1:
        result = '大吉!!!!'
    elif 2<=num<=4:
        result = '中吉!!'
    elif 5<=num<=8:
        result = '小吉'
    else:
        result = '凶'
    return render_template('result3.html',result = result)

if __name__ == '__main__':
    app.run(debug=True)