from flask_azure_oauth import FlaskAzureOauth
from flask_sqlalchemy import SQLAlchemy


# Database
db = SQLAlchemy()

# Auth
auth = FlaskAzureOauth()
