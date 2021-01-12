from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize Flask app.
app = Flask(__name__)

# Database URI
if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<username>:<password>@localhost/netflix?unix_socket=/cloudsql/<connection_name>"
else:
    # Used for unit/integration tests.
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB.
db = SQLAlchemy(app)

# Initialize Marshmallow.
ma = Marshmallow(app)
