from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    conn, cur = get_db()
    cur.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    post_list = cur.fetchall()
    return_list = []
    for post in post_list:
        post_dict = {
            'id': post[0],
            'title': post[1],
            'body': post[2],
            'created': post[3],
            'author_id': post[4],
            'username': post[5]
        }
        return_list.append(post_dict)
    return render_template('blog/index.html', posts=return_list)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            conn, cur = get_db()
            cur.execute('INSERT INTO post (title, body, author_id) VALUES ("%s", "%s", %s)' % (title, body, g.user['id']))
            conn.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(uid, check_author=True):
    conn, cur = get_db()
    cur.execute('SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON '
                 'p.author_id = u.id WHERE p.id = %s' % uid)
    result = cur.fetchone()

    if result is None:
        abort(404, "Post id {0} doesn't exist.".format(uid))

    if check_author and result[4] != g.user['id']:
        abort(403)
    post_dict = {
        'id': result[0],
        'title': result[1],
        'body': result[2],
        'created': result[3],
        'author_id': result[4],
        'username': result[5]
    }

    return post_dict


@bp.route('/<int:uid>/update', methods=('GET', 'POST'))
@login_required
def update(uid):
    post = get_post(uid)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            conn, cur = get_db()
            cur.execute('UPDATE post SET title = "%s", body = "%s" WHERE id = %s' % (title, body, uid))
            conn.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    conn, cur = get_db()
    cur.execute('DELETE FROM post WHERE id = %s' % id)
    conn.commit()
    return redirect(url_for('blog.index'))
