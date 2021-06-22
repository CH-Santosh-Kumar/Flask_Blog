import sqlite3
from flask import Flask, render_template,url_for,flash,redirect,request
from flask.helpers import url_for
from werkzeug import Request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect  


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Some secret Key'

@app.route("/")
def home():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template('home.html',posts=posts)


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html',post=post)

@app.route("/create",methods=('GET','POST'))
def create():
    print(f"Entered request {request.method}")

    if request.method == 'POST':
            print("Entered post")
            title = request.form['title']
            content = request.form['content']

            if not title:
                flash('Title is required!')
            else:
                print("entered else condition   ")
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                            (title, content))
                conn.commit()
                conn.close()
                return redirect(url_for('home'))

    return render_template('create.html')


@app.route("/<int:id>/edit", methods=('GET','POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if not title:
                flash('Title is required')
            else:
                conn = get_db_connection()
                conn.execute('UPDATE posts SET title = ? , content = ?'
                            'where id = ?',(title,content,id))
                conn.commit()
                conn.close()
                return redirect(url_for('home'))

    return render_template('edit.html',post=post)

@app.route("/<int:id>/delete", methods=('GET','POST'))
def delete(id):

    post =get_post(id)

    conn =get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))

    return redirect(url_for('home'))



if __name__=='__main__':
    app.run(debug=True)