# Standard library imports

# Standard library imports
import os

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Use environment variable if available
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config['SECRET_KEY'] = os.urandom(24)  # Set a secret key for sessions (important for production)

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

# Instantiate REST API
api = Api(app)

# Instantiate CORS (Cross-Origin Resource Sharing)
CORS(app, resources={r"/api/*": {"origins": "*"}})


