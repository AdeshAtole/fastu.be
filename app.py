import os
from flask import Flask, render_template

app = Flask('MyHerokuApp')

# We will set this up a bit later, do not worry if we leave it as None for now.
mailgun_secret_key_value = None

@app.route('/')
def index():

    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", value=mailgun_secret_key_value)

app.run(debug=True)
