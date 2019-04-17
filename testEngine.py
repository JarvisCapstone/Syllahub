#from sqlalchemy import create_engine
#engine = create_engine("mysql+pymysql://root:r9qi8nPF@localhost/Syellahub")
#print(engine)

import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# this userpass assumes you did not create a password for your database
# and the database username is the default, 'root'
userpass = 'mysql+pymysql://root:r9qi8nPF@'
basedir  = 'localhost' #'127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/Syllahub'
# this socket is going to be very different on a Windows computer
#socket   = '3306'
dbname   = dbname #+ socket

# put them all together as a string that shows SQLAlchemy where the database is
uri = userpass + basedir + dbname
app.config['SQLALCHEMY_DATABASE_URI'] = uri


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# this route will test the database connection and nothing more
@app.route('/')
def testdb():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return '<h1>It works.</h1>'
    except:
        return '<h1>Something is broken.</h1>'

if __name__ == '__main__':
    print(uri)
    app.run(debug=True)
    print('dd')
    db.session.query("1").from_statement("SELECT 1").all()
    print('<h1>It works.</h1>')
    
