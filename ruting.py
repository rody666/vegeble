from flask import Flask
import random
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/name/<user_name>')
def name(user_name):
    return f'Hello,{user_name}'

@app.route('/calculate/<int:a>/<int:b>')
def calculate(a,b):
    return str(a**b)

@app.route('/day/<int:num>')
def day(num):
    day_list = ['Mon','Tue','Wed','Thu','Fri','Stu','Sun']
    return 'Today is ' + day_list[num-1]

@app.route('/omikuji')
def omikuji():
    rnd = random.randint(1,10)
    if rnd == 1:
        return '大吉!!!!'
    elif 2<=rnd<=4:
        return '中吉!!'
    elif 5<=rnd<=8:
        return '小吉'
    else:
        return '凶'

if __name__ == '__main__':
    app.run(debug=True)

"""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


### タスクを表示する ###
@app.route("/", methods=["GET", "POST"])
def home():
    # データベースから全てのTodoレコードを取得
    todo_list = Todo.query.all()
    # 取得したTodoリストを"index.html"テンプレートに渡し、ウェブページとして表示
    return render_template("index.html", todo_list=todo_list)

### タスク追加 ###
@app.route("/add", methods=["POST"])
def add():
    # ユーザーから送信されたフォームデータからタイトルを取得
    title = request.form.get("title")
    # 新しいTodoオブジェクトを作成
    new_todo = Todo(title=title)
    # 新しいTodoをデータベースセッションに追加
    db.session.add(new_todo)
    # 変更をデータベースにコミット
    db.session.commit()
    # タスク追加後、ホームページにリダイレクト
    return redirect(url_for("home"))

### タスク削除 ###
@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    # URLから渡されたIDに基づいて、該当するTodoをデータベースから取得
    todo = Todo.query.filter_by(id=todo_id).first()
    # 取得したTodoをデータベースセッションから削除
    db.session.delete(todo)
    # 変更をデータベースにコミット
    db.session.commit()
    # タスク削除後、ホームページにリダイレクト
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
"""
