import json

"""
Using cookies with flask
========================
"""
from flask import (Flask, render_template, redirect,
                   url_for, request, make_response, flash)

from options import DEFAULTS

app = Flask(__name__)

# set a secret key for flash messages that are assigned to users
app.secret_key='asdflkj!23559086!fnasdfj&defln3'


def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'))  # get the character cookie if it exists

    except TypeError:
        data = {}
    return data


@app.route('/')
def index():
    data = get_saved_data()
    return render_template('index.html', saves=data)

@app.route('/builder')
def builder():
    return render_template(
        'builder.html',
        saves=get_saved_data(),
        options=DEFAULTS
    )


@app.route('/save', methods=['POST'])
def save():
    # import pdb; pdb.set_trace() can read data with pdb using request.form
    flash("Saved changes")
    response = make_response(redirect(url_for('builder')))  # redirect back to index
    data = get_saved_data()  # attempt to get the cookie if its stored
    data.update(dict(request.form.items()))  # update the cookie with whats on the form
    response.set_cookie('character', json.dumps(data))  # set the cookie
    return response


app.run(debug=True, host='0.0.0.0', port=8000)
