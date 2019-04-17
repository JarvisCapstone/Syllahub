import sys


sys.path.insert(0, '/var/www/html')

activate_this = '/usr/local/venvs/syllahub/bin/activate_this.py' 

# For Python 3
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from config import Config
from app import create_app

application = create_app(Config)




