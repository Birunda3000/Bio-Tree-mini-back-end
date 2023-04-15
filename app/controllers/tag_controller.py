from app import app
from ..service import *

@app.route("/")
def home():
    return "Hello World test!"

@app.route("/test")
def index():
    return "Hello World!"
