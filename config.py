import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    dialectDriver = "mysql"
    username = "root"
    password = "newpassword"
    host = "localhost"
    port = "3306"
    database = "syllahub"
    
    SQLALCHEMY_ECHO = True
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = "mysql://root:Winston@localhost:3306/Syllahub"
    #SQLALCHEMY_DATABASE_URI = "mysql://nick:temppassword@localhost:3306/syllahub"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:temppassword@localhost:3306/syllahub"
    #SQLALCHEMY_DATABASE_URI = "mysql://root:9UfhC%DHbC.G=tY.@localhost:3306/syllahub"
    #dialect+driver://username:password@host:port/database
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://JarvisSyllahub:databaseforall@JarvisSyllahub.mysql.pythonanywhere-services.com/JarvisSyllahub$Syllahub"
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
=======
>>>>>>> 752e9a048cda28661e890e3ddd39315680646d87
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = dialectDriver + "://" + \
                              username + ":" + \
                              password + "@" + \
                              host + ":" + \
                              port + "/" + \
                              database
    
    
