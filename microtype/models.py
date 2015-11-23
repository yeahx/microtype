import datetime
from pytype import db
from hashlib import md5
from mongoengine.queryset import queryset_manager
class User(db.Document):
    email = db.EmailField(required=True)
    nickname = db.StringField(max_length=20,required=True)
    password = db.StringField(max_length=48,required=True)
    about_me = db.StringField(max_length=255)

    def __repr__(self):
        return '<User %r>' % (self.email)

class Post(db.Document):
    created_at = db.DateTimeField(default = datetime.datetime.now)
    title = db.StringField(max_length=255, required=True)
    content = db.StringField(required=True)
    tag = db.StringField(required=True)
    author = db.ReferenceField(User)

    @queryset_manager
    def objects(cls, queryset):
        return queryset.order_by('-created_at')

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return '<Post %r>' % (self.title)

class Links(db.Document):
    url = db.StringField(max_length=255, required=True)
    text = db.StringField(max_length=255)

    def __unicode__(self):
        return self.url

    def __repr__(self):
        return '<Links %r>' % (self.url)