import os
import re

import googleapiclient.discovery
import googleapiclient.errors
from flask import Flask, render_template, redirect, make_response

from cachetools import cached, TTLCache

app = Flask('fastube')
tang_api_key = os.environ['GOOG_API_KEY_YT']
youtube_search_url = 'https://www.youtube.com/results?search_query='
youtube_video_url = 'https://www.youtube.com/watch?v='
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=tang_api_key)
id_cache = {}
cache_ttl = int(1*24*60*60)
cache_max_items = int(256*1024*1024/64)

robots_txt = open('static/robots.txt').read()
supported_separators_regex = re.compile(r'[.+= -,_]+')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/robots.txt')
def robots():
    response = make_response(robots_txt)
    response.headers["Content-type"] = "text/plain"
    return response


@app.route('/<query>')
def lucky(query):
    q = re.sub(supported_separators_regex, ' ', query)
    return fortunate(q)


@cached(TTLCache(cache_max_items, cache_ttl))
def fortunate(query):
    request = youtube.search().list(
    part="snippet",
    maxResults=1,
    q=query,
    type="video"
    )
    response = request.execute()
    if len(response['items']) == 0:
        return render_template("notfound.html")
    video_id = response['items'][0]['id']['videoId']
    print('Picked from API for: ' + query)
    return redirect(youtube_video_url + video_id, code=302)


@app.route('/s/<query>')
def search(query):
    return redirect(youtube_search_url +
                    re.sub(supported_separators_regex, '+', query), code=302)
