import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/CMPUT401-FenceFriends/fencing")

from app import app as application
application.secret_key = 'secret'