from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form2.html')

@app.route('/result',methods=['POST'])
def result():
    value1 = int(request.form['value1'])
    value2 = int(request.form['value2'])
    output1 = f'{value1}+{value2}={value1+value2}'
    output2 = f'{value1}*{value2}={value1*value2}'
    return output1 +"<br>"+ output2

app.run(debug=True)