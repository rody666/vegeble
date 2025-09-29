from flask import Flask, request, render_template

app = Flask(__name__)
memos = []
id = 0
@app.route('/')
def index():
    return render_template('memo.html')

@app.route('/add',methods=['post'])
def add():
    title = request.form['title']
    text = request.form['text']
    tmp = {'id':id,'title':title,'text':text}
    memos.append(tmp)
    print(memos)
    return render_template('memo.html',memos=memos)

if __name__ == '__main__':
    app.run(debug=True)