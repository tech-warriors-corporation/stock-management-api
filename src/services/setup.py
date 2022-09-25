from flask import Flask
from flask_cors import CORS
from src.utils.constants import api_prefix

app = Flask(__name__)

CORS(app, resources={rf"/{api_prefix}/*": { "origins": ["https://sistema-de-estoque-projeto-casulo.netlify.app", "http://localhost:4200"] }})
