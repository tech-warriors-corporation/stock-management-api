from src.services.setup import app
from os import environ
from src.enums.env_var import EnvVar
import src.routes.auth

app.run(debug=eval(environ.get(EnvVar.DEBUG_MODE.value)))
