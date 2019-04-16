import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    dialectDriver = "mysql" # use "mysql+pymysql" on linux
    username = "root"
    password = "newpassword"
    host = "localhost"
    port = "3306"
    database = "syllahub"
    
    #SQLALCHEMY_ECHO = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = dialectDriver + "://" + \
                              username + ":" + \
                              password + "@" + \
                              host + ":" + \
                              port + "/" + \
                              database
    
    
class ProductionConfig(object):
    #TODO
    pass
