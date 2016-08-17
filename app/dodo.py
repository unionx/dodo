#!/usr/bin/env python3
from flask import Flask, Response, render_template, request
import requests
import hashlib
import redis

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "UNIQUE_SALT"
default_name = "unionx"


@app.route('/', methods=['GET', 'POST'])
def hello():
    name = default_name
    if request.method == 'POST':
        name = request.form['name']

    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    return render_template('index.html', input_text=name, name_hash=name_hash)


@app.route('/monster/<name>')
def get_identicon(name):
    img = cache.get(name)
    if img is None:
        print("Cache miss")
        r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
        img = r.content
        cache.set(name, img)

    return Response(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
