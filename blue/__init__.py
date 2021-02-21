from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api,Resource

app = Flask(__name__)
CORS(app)

from blue.api.routes import mod 

app.register_blueprint(api.routes.mod,url_prefix = '/api')
