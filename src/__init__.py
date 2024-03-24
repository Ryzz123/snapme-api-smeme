from flask import Flask
from src.routes.route import Route
from src.app.app import App
from flask_cors import CORS

# Create an instance of the Flask class for our web app.
flask_app = Flask(__name__)

# Enable Cross Origin Resource Sharing (CORS) for the Flask app.
# This allows the server to respond to requests from different origins.
CORS(flask_app)

# Wrap the Flask app instance with our custom App class.
# This could be used to add additional configuration or functionality to the Flask app.
app = App(flask_app)

# Initialize the Route class with our app instance.
# This is likely where the routes for our web app are defined.
Route(app)
