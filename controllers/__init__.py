from flask import Blueprint

# Create a blueprint for the controllers
controllers_bp = Blueprint('controllers', __name__)

# Import the controller files to register their routes
from . import auth, investments, portfolio
