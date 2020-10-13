from flask import Flask

app = Flask(__name__)

from air_pollutionapp import routes
