import pip

if int(pip.__version__.split('.')[0])>9:
    from pip._internal import main
else:
    from pip import main


_all_ = [
    "alembic>=1.0.7",
    "beautifulsoup4>=4.7.1",
    "certifi>=2019.3.9",
    "chardet>=3.0.4",
    "Click>=7.0",
    "Faker>=1.0.4",
    "Flask>=1.0.2",
    "Flask-Login>=0.4.1",
    "Flask-Migrate>=2.4.0",
    "Flask-SQLAlchemy>=2.3.2",
    "Flask-WTF>=0.14.2",
    "html5lib>=1.0.1",
    "idna>=2.8",
    "itsdangerous>=1.1.0",
    "Jinja2>=2.10.1",
    "lxml>=4.3.3",
    "Mako>=1.0.7",
    "MarkupSafe>=1.1.0",
    "numpy>=1.16.2",
    "pandas>=0.24.2",
    "PyMySQL>=0.9.3",
    "python-dateutil>=2.8.0",
    "python-dotenv>=0.10.1",
    "python-editor>=1.0.4",
    "pytz>=2019.1",
    "six>=1.12.0",
    "soupsieve>=1.9",
    "SQLAlchemy>=1.2.18",
    "SQLAlchemy-Utils>=0.33.11",
    "text-unidecode>=1.2",
    "urllib3>=1.24.1",
    "webencodings>=0.5.1",
    "Werkzeug>=0.14.1",
    "WTForms>=2.2.1",
    "fpdf>=1.7.2",
]

windows = [
    "mysqlclient==1.4.2.post1",
]

linux = []

darwin = []

def install(packages):
    for package in packages:
        main(['install', package])

def runMigrations():
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("migrations/alembic.ini")
 
    from config import Config as AppConfig

    appConfig = AppConfig()
    dbURI = appConfig.SQLALCHEMY_DATABASE_URI
    print(dbURI)

    from app import create_app, db

    app = create_app()

    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate, upgrade
    from flask_script import Manager
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', upgrade)
    manager.run()
    #from sqlalchemy import create_engine
    #engine = create_engine(dbURI)
    #print(engine)
    #with engine.begin() as connection:
    #    alembic_cfg.attributes['connection'] = connection
    #    command.upgrade(alembic_cfg, "head")
    #print('success')

if __name__ == '__main__':

    from sys import platform

    #install(_all_) 
    if platform == 'windows':
        install(windows)
    if platform.startswith('linux'):
        install(linux)
    if platform == 'darwin': # MacOS
        install(darwin)

    #runMigrations()

