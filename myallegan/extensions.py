from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_wtf import CsrfProtect


# Data and workers.
db = SQLAlchemy()

# Utilities.
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
csrf = CsrfProtect()
