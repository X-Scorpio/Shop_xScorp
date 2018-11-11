# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
path = '/home/XScorpio/StoneCampus'
if path not in sys.path:
    sys.path.insert(0, path)

# import flask app but need to call it "application" for WSGI to work
from shop import app as application  # noqa
