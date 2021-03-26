import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_DATABASE_URI = 'postgresql://fyyredbuser:fyyredbpass@localhost:5432/fyyredb'
DATABASE_NAME = "fyyredb"
username = "fyyredbuser"
password = "fyyredbpass"
url = "localhost:5432"
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(username,password,url,DATABASE_NAME)
