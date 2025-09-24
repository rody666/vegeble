from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


### タスクを表示する ###

### タスク追加 ###

### タスク削除 ###


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

