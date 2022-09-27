from os import environ
from enums.env_var import EnvVar
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_cors import CORS
from utils.constants import api_prefix

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={rf"/{api_prefix}/*": { "origins": [environ.get(EnvVar.ORIGIN.value)] }})

import routes.auth

if __name__ == '__main__':
    app.run(debug=eval(environ.get(EnvVar.DEBUG_MODE.value)))
