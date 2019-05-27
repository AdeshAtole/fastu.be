import os
import re

import googleapiclient.discovery
import googleapiclient.errors
from flask import Flask, render_template, redirect

app = Flask('fastube', static_folder='static', static_url_path='')
tang_api_key = os.environ['GOOG_API_KEY_YT']
youtube_search_url = 'https://www.youtube.com/results?search_query='
youtube_video_url = 'https://www.youtube.com/watch?v='
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey = tang_api_key)
id_cache = {}

supported_separators_regex = re.compile(r'[.+= -,_]+')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<query>')
def lucky(query):
    q=re.sub(supported_separators_regex ,  ' ' , query)

    if q in id_cache:
        video_id = id_cache[q]
        print ('Picked from cache for ' + q)
    else:
        request = youtube.search().list(
            part="snippet",
            q=q,
            type="video"
        )
        response = request.execute()
        if len(response['items']) == 0:
            return render_template("notfound.html")
        video_id = response['items'][0]['id']['videoId']
        id_cache[q] = video_id
        print 'Picked from API for ' + q
        
    return redirect(youtube_video_url + video_id, code=302 )



@app.route('/s/<query>')
def search(query):
    return redirect(youtube_search_url + re.sub(supported_separators_regex ,  '+' , query) , code=302)