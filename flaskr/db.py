import sqlite3
import MySQLdb

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'mysql_cur' in g and 'mysql_conn' in g:
        return g.mysql_conn, g.mysql_cur
    else:
        g.mysql_conn = MySQLdb.connect(host='192.168.18.11', user='root', passwd='123456',
                                       db='baggins', port=3306, use_unicode=True, charset='utf8')
        g.mysql_cur = g.mysql_conn.cursor()
        return g.mysql_conn, g.mysql_cur
    #if 'db' not in g:
    #    g.db = sqlite3.connect(
    #        current_app.config['DATABASE'],
    #        detect_types=sqlite3.PARSE_DECLTYPES
    #    )
    #    g.db.row_factory = sqlite3.Row

    #return g.db


def db_try():
    mysql_conn = MySQLdb.connect(host='192.168.18.11', user='root', passwd='123456',
                                   db='baggins', port=3306, use_unicode=True, charset='utf8')
    mysql_cur = mysql_conn.cursor()
    mysql_cur.execute('select * from baggins_works')
    print mysql_cur.fetchall()



def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

if __name__ == '__main__':
    db_try()
