from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.secret_key = "My Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(port=5001,debug=True)
