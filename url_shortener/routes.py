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

@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)

    # if url is saved in database
    if original_id:
        original_id = original_id[0]
        # retrive url using the id
        url_data = conn.execute('SELECT original_url, clicks FROM urls WHERE id = (?)', (original_id,)).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks'] + 1
        # update clicks count in DB
        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?', (clicks, original_id))
        conn.commit()
        conn.close()
        return redirect(original_url)
    #If url is not saved on DB
    else:
        flash('Invalid URL!')
        return redirect(url_for('index'))

@app.route('/stats')
def stats():
    conn = get_db_connection()

    db_urls = conn.execute('SELECT id, created, original_url, clicks FROM urls').fetchall()

    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    return render_template('stats.html', urls=urls)