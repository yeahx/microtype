import random
import string
from hashlib import md5
from flask import session, flash, redirect, url_for
from models import User
from functools import wraps
import models
import forgery_py

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def generate_csrf_token():
    #if '_csrf_token' not in session:
    session['_csrf_token'] = random_string(size=16)
    return session['_csrf_token']

def check_user_password(username, password):
    user = User.objects(email=username).first()
    return user.password == md5(password).hexdigest()

def gen_user_passwrod(password):
    return md5(password).hexdigest()

def generate_fake(count=100,tag="Python",user=None):
    random.seed()
    for i in range(count):
        p = models.Post(content=forgery_py.lorem_ipsum.sentences(random.randint(1,3)),tag=tag,author=user,title=forgery_py.lorem_ipsum.title())
        p.save()

def login_required():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get('user'):
                flash('You must be logged in..', 'error')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper