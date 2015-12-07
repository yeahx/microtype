#!/usr/bin/env python

from microtype import app
from microtype import models,db
from microtype.helper_functions import generate_fake
from flask.ext.script import Manager, Shell, Server

manager = Manager(app)

def make_shell_context():
    return dict(models=models,app=app,db=db,generate_fake=generate_fake)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    port=80,
    host="0.0.0.0"
)
)

if __name__ == "__main__":
    manager.run()
