from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.memo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(128), nullable=False)

@app.route('/')
def index():
    return render_template('memo2.html')

if __name__ == '__main__':
    #app.run()
    db.create_all()