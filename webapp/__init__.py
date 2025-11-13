from flask import Flask
from flask_login import LoginManager
from flask_limiter import Limiter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
limiter = Limiter(app)

from webapp.routes import auth_route, todo_route