from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
import os 

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/krea_reqruiter?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this-is-the-secret-key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)

# Init JWT
jwt = JWTManager(app)
# Init DB
db = SQLAlchemy(app)

# Run Server
if __name__ == "__main__":
    from api import *
    app.run(port=8000,debug=True)