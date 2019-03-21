import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    dialectDriver = "mysql"
    username = "root"
    password = "rootpw"
    host = "localhost"
    port = "3306"
    database = "Syllahub"
    
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = dialectDriver + "://" + \
                              username + ":" + \
                              password + "@" + \
                              host + ":" + \
                              port + "/" + \
                              database 
