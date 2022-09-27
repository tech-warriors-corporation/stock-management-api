from os import environ
from enums.env_var import EnvVar
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_cors import CORS
from utils.constants import api_prefix

load_dotenv(find_dotenv())

app = Flask(__name__)

CORS(app, resources={rf"/{api_prefix}/*": { "origins": [environ.get(EnvVar.ORIGIN.value)] }})

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', environ.get(EnvVar.ORIGIN.value))
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')

  return response

import routes.auth

if __name__ == '__main__':
    app.run(debug=eval(environ.get(EnvVar.DEBUG_MODE.value)))
