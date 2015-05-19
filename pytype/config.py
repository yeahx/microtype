import os
from datetime import timedelta
CSRF_ENABLED = True
BLOG_TITLE = r"Nightraid's Blog"
SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZjViZWY0OTc1ZWVjZTdkMGZkN2EyZmJiZjEwOTBjNTM='
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
MONGODB_SETTINGS = {
    'db': 'blog',
    'host': '192.168.16.66',
    'port': 27017,
    'username': 'example',
    'password': 'example'
}