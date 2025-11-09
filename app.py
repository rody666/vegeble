from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from openai import OpenAI
import os
import base64
from api_key import apikey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import uuid
import json

app = Flask(__name__)
app.secret_key = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://prices.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://messages.db'
client = OpenAI(api_key=apikey.key)
db = SQLAlchemy(app)

prompt = """
You are a vegetable assessment AI. Follow these rules strictly:

1. Input: the name of the vegetable and a short description of its condition.
2. Output must be in valid JSON format only, in one line.
3. JSON must contain the following three keys:
   - "vegetable": the name of the vegetable (in Japanese)
   - "condition": a number between 0.0 and 1.0 
       (0 = unsellable, 1 = perfect, like supermarket quality)
   - "reason": 
       - If the condition is 0.7 or lower, describe the reason in Japanese (e.g., "傷がある", "色が悪い").
       - If the condition is higher than 0.7, output "none".
4. Keep the output concise and consistent with the examples.
5. Examples:
   Input: "Tomato, slightly wilted"
   Output: {"vegetable": "トマト", "condition": 0.7, "reason": "少ししなびている"}
   Input: "Cabbage, firm leaves, no damage"
   Output: {"vegetable": "キャベツ", "condition": 1.0, "reason": "none"}

Input: "{vegetable_description}"
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(200))
    user_type = db.Column(db.String(20))  # 'farmer' or 'employee'
    created_at = db.Column(db.DateTime, default=datetime.now)

class Vegetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    base_price = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.now)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vegetable_id = db.Column(db.Integer, db.ForeignKey('vegetable.id'))
    image_path = db.Column(db.String(200))
    condition = db.Column(db.String(100))
    weight = db.Column(db.Float)
    price_per_kg = db.Column(db.Float)
    total_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.now)
    is_read = db.Column(db.Boolean, default=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    agreed_price = db.Column(db.Float)
    pickup_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    updated_at = db.Column(db.DateTime, default=datetime.now)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_name = db.Column(db.String(100))
    upload_at = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

def price(image_type,image_base64):
    image_data_url = f"data:image/{image_type};base64,{image_base64}"
    try: 
        response = client.responses.create(
            model="gpt-5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text","text": prompt,},
                        {"type": "input_image","image_url": image_data_url}
                    ]
                }
            ]
        )
        return response.output_text
    except Exception as e:
        # Capture full traceback so the runtime error can be inspected
        import traceback
        tb = traceback.format_exc()
        # Print to console (Flask dev server stdout) and return so the template can show it
        print("Error in price():", tb)
        return f"ERROR in price(): {e}\n{tb}"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'heif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('assessment.html')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        user = User.query.filter_by(phone=phone,password_hash=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return 'ログイン失敗'
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        if User.query.filter_by(phone=phone).first():
            return 'この電話番号はすでに登録されています。'
        user = User(name=name, phone=phone, password_hash=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['vege_image']
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        uniqID = uuid.uuid4().hex
        image = Image(user_id = session['user_id'], image_name = f'{uniqID}.{ext}')
        db.session.add(image)
        db.session.commit()
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            f'{uniqID}.{ext}'
        )
        file.save(filepath)
        return jsonify({"status":"ok", "filename": f'{uniqID}.{ext}'})
    return ''

@app.route('/assessment/<string:filename>', methods=['GET','POST'])
def assessment(filename):
    image = Image.query.filter_by(image_name=filename).first()
    if image:
        path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        output = price(filename.rsplit('.', 1)[1], encoded)
        return jsonify(json.loads(output))
    else: 
        return (f'{filename} is Not exist')


@app.route('/mypage', methods=['GET','POST'])
def mypage():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template(
        'mypage.html',
        name=user.name, 
        phone=user.phone, 
        password=user.password_hash, 
        date=user.created_at
        )

@app.route('/logout')
def logtou():
    session.clear()
    return redirect(url_for('login'))

@app.route('/setprice')
def setprice():
    vegetables = Vegetable.query.all()
    return render_template('setprice.html',vegetables=vegetables)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/uploads')
def uploads():
    uploads = Image.query.all()
    return render_template('uploads.html', uploads=uploads)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
