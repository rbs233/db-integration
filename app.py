from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, drop_database, create_database
import settings
import os
import click
from flask.cli import with_appcontext

DATABASE_URL = os.getenv('DATABASE_URL') + '/hello_world' 
app = Flask(__name__)
app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = DATABASE_URL,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
db = SQLAlchemy(app)

from models import *

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/createuser')
def createuser():
    name = request.args.get('name', None)
    token = request.args.get('access_token', None)
    u = User(name, token)
    db.session.add(u)
    db.session.commit()
    return 'user {} created'.format(name)

@app.route('/listusers')
def listusers():
    user_list = User.query.order_by(User.id).all()
    if user_list:
        return_string = 'All users: '
        for u in user_list:
            return_string += '{}, {}, {};'.format(u.id, u.name, u.access_token)
    else:
        return_string = 'No Users in Database'

    return return_string

@app.cli.command()
def initdb():
    ### If database exists, drop it
    if database_exists(DATABASE_URL):
        drop_database(DATABASE_URL)
        click.echo('existing database dropped')

    ### create database and table
    create_database(DATABASE_URL)
    db.create_all()
    click.echo("database initialized")

if __name__ == '__main__':
    app.run()
