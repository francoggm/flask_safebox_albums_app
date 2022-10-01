from flask import Flask
from base64 import b64encode
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'random-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from .auth import users
from .views import views

app.register_blueprint(users)
app.register_blueprint(views)
app.jinja_env.globals.update(len=len, bs4enc=b64encode)

from .models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
