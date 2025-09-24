from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'test update'

if __name__ == "__main__":
    app.run(debug=True)