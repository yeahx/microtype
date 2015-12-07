#-*- coding:utf-8 -*-
import datetime
from flask import render_template,request,g,flash,redirect,url_for,session,Response
from werkzeug.contrib.atom import AtomFeed
from microtype.main import main
from microtype.models import Post,User
from microtype.helper_functions import login_required,gen_user_passwrod
from microtype.config import BLOG_TITLE

@main.route("/")
@main.route("/index/<int:page>")
def index(page=1):
    pagination = Post.objects.paginate(page=page, per_page=3)
    posts = pagination.items
    return render_template('index.html', title = "Index | "+ BLOG_TITLE, posts = posts, pagination = pagination)

@main.route("/post/<title>")
def posts(title=None):
    post = Post.objects.get_or_404(title=title)
    return render_template('post.html',title = post.title+" | "+BLOG_TITLE, post = post)

@main.route("/links")
def links():
    return render_template("links.html", title = "Links | "+ BLOG_TITLE)

@main.route("/user/<username>")
@login_required()
def user(username = None):
    user = User.objects.get_or_404(nickname = username)
    return render_template("profile.html", profile=user, title= "Profile | "+BLOG_TITLE, username=session.get("nickname"))

@main.route("/editprofile/<username>", methods=["get","post"])
@login_required()
def editprofile(username = None):
    user = User.objects.get_or_404(nickname = username)
    if request.method == "POST":
        about_me = request.form.get("about_me")
        pass1 = request.form.get("password1")
        pass2 = request.form.get("password2")
        nickname = request.form.get("nickname")
        if about_me and nickname:
            user.about_me = about_me
            user.nickname = nickname
            session["nickname"] = nickname
            if pass1 == None and pass2 == None:
                user.save()
            elif pass1 == pass2 and pass1 and pass2 != None:
                user.password = gen_user_passwrod(pass1)
                print user.password
                user.save()
            else:
                user.save()
            flash(u"修改成功", "success")
        else:
            flash(u"错误", "error")

    return render_template("editprofile.html", profile=user, title="Edit | "+BLOG_TITLE, username=session.get("nickname"))

@main.route("/admin")
@login_required()
def admin():
    return render_template("admin.html", title = "Admin | "+ BLOG_TITLE)

@main.route("/admin/newpost", methods=["post","get"])
@login_required()
def newpost():
    if request.method == "POST":
        posttitle = request.form.get("title")
        posttag = request.form.get("tag")
        posthtml = request.form.get("content")
        author = User.objects(email=g.user).first()
        if request.form.get("post-id"):
            post = Post.objects(id=request.form.get("post-id")).first()
            post.title = posttitle
            post.tag = posttag
            post.content = posthtml
            post.author = author
            post.created_at = datetime.datetime.now
            post.save()
            flash("Update success..","success")
        else:
            post = Post(title=posttitle, content = posthtml, tag=posttag, author = author)
            post.save()
            flash("Add success..","success")

    return render_template("newpost.html", title = "New Post | "+BLOG_TITLE)

@main.route("/admin/postlist/<int:page>")
@login_required()
def postlist(page=1):
    pagination = Post.objects.paginate(page=page, per_page=5)
    session['page'] = request.path.split('/')[3]
    posts = pagination.items
    return render_template("postlist.html", title = "Posts | "+ BLOG_TITLE, posts = posts, pagination = pagination)

@main.route("/admin/editpost/<id>")
@login_required()
def editpost(id=None):
    post = Post.objects(id=id).first()
    return render_template("editpost.html", title="Editpost | "+BLOG_TITLE, post=post)

@main.route("/admin/removepost/<id>")
@login_required()
def removepost(id=None):
    if Post.objects().count() > 1:
        post = Post.objects(id=id)
        post.delete()
        print session.get("page")
        flash("Remove success..",'success')
        return redirect(url_for("main.postlist", page=session.get("page")))
    else:
        flash("Need to be at least one post..", 'error')

@main.route("/admin/settings")
@login_required()
def settings():
    pass

@main.route("/tags/<tag>")
def tags(tag = None):
    posts = Post.objects(tag=tag)
    tags = Post._get_collection().aggregate([
        {'$group':{'_id':'$tag','count':{'$sum':1}}},
        {'$sort':{'count': -1}},
        {'$limit': 10}
    ])
    tags = tags["result"]
    return render_template("tags.html", title = "Tags | "+ BLOG_TITLE, posts = posts, tags = tags)

@main.route("/feed")
def feed():
    _feed = AtomFeed(title = BLOG_TITLE,
                     icon = r"http://www.rdoge.cc/static/favicon.ico",
                     url=request.url_root
                     )

    posts = Post.objects[:12]

    for _post in posts:
        _feed.add(
            title = _post.title,
            content = _post.content,
            content_tyep = "html",
            author = _post.author.nickname,
            url = url_for("main.posts", title=_post.title, _external=True),
            published = _post.created_at,
            updated = _post.created_at
        )

    return Response(_feed.to_string(), mimetype="application/xml")

@main.app_errorhandler(404)
def page_not_found(error):
   return render_template("404.html", title = "Not found | "+BLOG_TITLE)


@main.app_template_filter('formatdate')
def format_datetime_filter(input_value, format_="%Y/%m/%d"):
    return input_value.strftime(format_)
