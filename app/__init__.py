from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='../static')
app.secret_key = 'your_secret_key'  # 确保已设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'  # SQLite 数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes

with app.app_context():
    db.create_all()  # 创建数据库表