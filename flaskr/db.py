import os
import click
import mysql.connector

from flask.cli import with_appcontext
from flask import current_app, g
from dotenv import load_dotenv

load_dotenv()

def get_db():
    if 'db' not in g:
        g.db=mysql.connector.connect(
            host="db",
            user="wyllis",
            password="wyllis",
            database="processor",
            auth_plugin='mysql_native_password'
        )

    return g.db


def close_db(event=None):
    database = g.pop('db', None)

    if database is not event:
        database.close()

def init_db():
    database = get_db()

    with current_app.open_resource('schema.sql') as file:
        db_cursor = database.cursor()
        db_cursor.execute(file.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
