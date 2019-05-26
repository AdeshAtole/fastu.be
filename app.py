import os
import re

import googleapiclient.discovery
import googleapiclient.errors
from flask import Flask, render_template, redirect

app = Flask('fastube')
tang_api_key = os.environ['GOOG_API_KEY_YT']
youtube_search_url = 'https://www.youtube.com/results?search_query='
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey = tang_api_key)

supported_separators_regex = re.compile(r'[.+= -,_]+')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<query>')
def lucky(query):
    q=re.sub(supported_separators_regex ,  ' ' , query)
    request = youtube.search().list(
        part="snippet",
        q=q,
        type="video"
    )
    response = request.execute()
    
    return "hello " + query + ' ' + os.environ['ADESH']  + ' ' + str(response['items'][0])



@app.route('/s/<query>')
def search(query):

    # We will just display our mailgun secret key, nothing more.
    return redirect(youtube_search_url + re.sub(supported_separators_regex ,  '+' , query) , code=302)
    # return youtube_search_url + re.sub(supported_separators_regex ,  '+' , query)
#app.run(debug=True)
