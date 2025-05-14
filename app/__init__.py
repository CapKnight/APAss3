from flask import Flask

app = Flask(__name__, static_folder='../static')
app.secret_key = '12345'

from app import routes