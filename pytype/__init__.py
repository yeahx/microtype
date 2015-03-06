from flask import Flask
from flask.ext.mongoengine import MongoEngine
from . import config


app = Flask(__name__)
app.config.from_object(config)
db = MongoEngine(app)
from helper_functions import generate_csrf_token
from pytype.models import Post
from pytype.models import User
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.jinja_env.globals['csrf_token'] = generate_csrf_token
app.jinja_env.globals['tags'] = Post._get_collection().aggregate([{'$group':{'_id':'$tag','count':{'$sum':1}}},{'$sort':{'count': -1}},{'$limit': 10}])['result']
app.jinja_env.globals['recent_posts'] = Post.objects[:5]
app.jinja_env.globals['about_me'] = User.objects.get(email="shadowxqq@gmail.com")