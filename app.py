import os
import re

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from flask import Flask, render_template, redirect

app = Flask('MyHerokuApp')
youtube_search_url = 'https://www.youtube.com/results?search_query='

supported_separators_regex = re.compile(r'[.+= -,_]+')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<query>')
def lucky(query):
    return "hello " + query + ' ' + os.environ['PORT'] 



@app.route('/s/<query>')
def search(query):

    # We will just display our mailgun secret key, nothing more.
    return redirect(youtube_search_url + re.sub(supported_separators_regex ,  '+' , query) , code=302)
    # return youtube_search_url + re.sub(supported_separators_regex ,  '+' , query)
#app.run(debug=True)
