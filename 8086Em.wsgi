import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/8086Em')

from main import app as application
application.secret_key = ''
