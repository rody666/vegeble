from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
memos = []
id = 0

@app.route('/')
def index():
    return render_template('memo.html',memos=memos)

@app.route('/add',methods=['post'])
def add():
    global id
    title = request.form['title']
    text = request.form['text']
    tmp = {'id':id,'title':title,'text':text}
    memos.append(tmp)
    id += 1
    return redirect(url_for('index'))

@app.route('/delete', methods=['post'])
def delete():
    delete_id = request.form['id']
    for i in range(len(memos)):
        if str(memos[i]['id']) == delete_id:
            memos.pop(i)
            break
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)