from utils.error import customized_error

app = None

try:
    app = __import__("app").app
except:
    customized_error("app")

try:
    app = __import__("__main__").app
except:
    customized_error("__main__")
