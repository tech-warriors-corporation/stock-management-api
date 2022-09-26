from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_cors import CORS
from src.utils.constants import api_prefix
from os import environ
from src.enums.env_var import EnvVar

load_dotenv(find_dotenv())

app = Flask(__name__)

CORS(app, resources={rf"/{api_prefix}/*": { "origins": [environ.get(EnvVar.ORIGIN.value)] }})
