from flask_mysqldb import MySQL
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config/config.py')

mysql = MySQL(app)
