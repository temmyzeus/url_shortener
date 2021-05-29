from url_shortener import app
from url_shortener import get_db_connection
from flask import render_template, request, flash, redirect, url_for
from url_shortener import hashids

@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        # incase the input field is empty
        if not url:
            flash('URL is Required!')
            return redirect(url_for('index'))

        # insert url into last row in DB
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid #join host url and link id to create link for url

        return render_template('index.html', short_url=short_url)
        
    return render_template('index.html')