from src.services.setup import app
from dotenv import load_dotenv, find_dotenv
from os import environ
from src.enums.env_var import EnvVar

load_dotenv(find_dotenv())

import src.routes.auth

app.run(debug=eval(environ.get(EnvVar.DEBUG_MODE.value)))
