from flask import Flask
from src.routes.route import Route
from src.app.app import App
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app = App(app)
Route(app)
