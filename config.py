from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
 
app = Flask(__name__)
bcrypt = Bcrypt
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rsyh2y9d'
app.config['MYSQL_DATABASE_DB'] = 'bd_devfruit'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['SECRET_KEY'] = 'thisisasecretkey'
mysql.init_app(app)
 
conn = mysql.connect()
cursor =conn.cursor()
#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
FLASK_APP='app.py'
FLASK_ENV='development'
DEBUG = True