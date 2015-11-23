# -*- coding: utf8 -*-
from . import auth
from flask import render_template,request,flash,redirect,url_for,session,abort,g
from pytype.models import User
from pytype.config import BLOG_TITLE
from pytype.helper_functions import check_user_password,login_required

@auth.route("/login", methods = ["POST", "GET"])
def login():
    session.permanent = True
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.objects(email=username).first()
        if user is not None and check_user_password(username,password):
            session['user'] = username
            session['nickname'] = user.nickname
            flash("login success!", 'success')
            return redirect(url_for("main.index"))
        else:
            flash("username or password falid!", 'error')
            return redirect(url_for("auth.login"))
    else:
        if session.get('user'):
            flash("you are already logged in!", 'error')
            return redirect(url_for('main.index'))

    return render_template("auth/login.html", title="Login | "+ BLOG_TITLE)

@auth.route("/logout")
@login_required()
def logout():
    session.pop('user')
    flash(" You are logged out!","success")
    return redirect(url_for('main.index'))

@auth.before_app_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form['_csrf_token']:
            abort(404)

@auth.before_app_request
def before_request():
    g.user = session.get("user")
    g.nickname = session.get("nickname")