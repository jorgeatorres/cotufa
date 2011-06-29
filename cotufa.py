# -*- coding: utf-8 -*-
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

# setup app
app = Flask(__name__)
app.config.from_pyfile('cotufa.cfg')

db = SQLAlchemy(app)

import model
from views import *

def bootstrap():
    print 'Dropping database tables...'
    db.drop_all()

    print 'Creating database tables...'
    db.create_all()

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2 and sys.argv[1] == 'bootstrap':
        bootstrap()
    else:
    	app.run()
