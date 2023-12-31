import os
import sqlite3

import dotenv
from flask import Flask, render_template, request, url_for, flash, redirect
from pathlib import Path
from werkzeug.exceptions import abort

dotenv.load_dotenv()

app = Flask(__name__)
# Set this in a .env file (see README.md)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
data_dir = Path(__file__).parent.joinpath('data')


@app.errorhandler(404)
def not_found_error(error): return render_template('404.html'), 404


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    this_post = get_post(post_id)
    return render_template('post.html', post=this_post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


# ....

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


def get_post(post_id):
    conn = get_db_connection()
    this_post = conn.execute('SELECT * FROM posts WHERE id = ?',
                             (post_id,)).fetchone()
    conn.close()
    if this_post is None:
        abort(404)
    return this_post


def get_db_connection():
    """
       Creates and returns a connection to the database.

       :return: A connection object that allows interaction with the database.
       :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect(data_dir.joinpath('database.db'))
    # This means that the database connection will return rows that behave like regular Python dictionaries.
    conn.row_factory = sqlite3.Row
    return conn
