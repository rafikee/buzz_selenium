import requests
from dateutil.parser import parse
import logging
import re

def get_videos(data):

    base_url = "http://mm.apptek.com:8983/solr/media/select" #URL for sending the GET request
    media_url = "http://mm.apptek.com/media" # URL prefix that sends us straight to the mp4
    apptek_url = "http://mm.apptek.com/tv/watch?id=" # URL prefix that sends us to the video in the UI
    time_concat = ":00Z" # Solr wants datetime to end with this

    channel = data['channel'] # Channel parameter as specified by user
    language = 'ar' # Language code to be passed in GET request
    results_limit = data['limit'] # limit the number of rows we get in response from IdenTV (specified by user)
    start_date = data['start_date'] + time_concat # datetime string to be passed to GET request
    end_date = data['end_date'] + time_concat # datetime string to be passed to GET request

    query = data['query'] # query input by user
    query = query.split('\r\n') #query takes multiline form, place each segment as item in array

    search_tokens = ' '.join(query)
    search_tokens = [x for x in search_tokens.split('"') if x and not x.isspace()]
    search_tokens = '|'.join(search_tokens)
    search_tokens = search_tokens.replace("*", r"\w*")
    pattern = re.compile(search_tokens)

    for i, line in enumerate(query):
        line = [x for x in line.split('"') if x and not x.isspace()]
        for x, phrase in enumerate(line):
            if ' ' in phrase:
                line[x] = phrase.replace(" ", " AND ")
        line = ["(" + x + ")" for x in line]
        line = " OR ".join(line)
        query[i] = "seg_ar:(" + line + ")"
    query = " AND ".join(query)

    print(query)

    q = 'source:' + channel + ' AND ' + 'lang:' + language + ' AND ' + query

    payload = {
        'q' : q,
        'wt' : 'json',
        'sort' : 'start_dt desc',
        'rows' : results_limit,
        #'fl' : 'start_dt,end_dt,duration,media,' + 'seg_' + language,
        'fl' : 'start_dt,media,seg_ar',
        'fq' : 'start_dt:[' + start_date + ' TO ' + end_date + ']',
    }

    r = requests.get(base_url, params = payload)
    data = r.json()

    #[something for segment in clip['seg_ar']]

    payload = [
        {
            'video_url' : apptek_url + clip['media'],
            'tokens' : pattern.findall(' '.join(clip['seg_ar'])),
        }
        for clip in data['response']['docs']
    ]

    #video_urls = [apptek_url + clip['media'] for clip in data['response']['docs']]

    ''' If we want MP4 and link to IDENTV

    video_urls = [
        {
            'mp4' : "/".join((media_url, channel, parse(clip['start_dt']).date().strftime('%Y/%m/%d'), clip['media'] + '.mp4')),
            'apptek' : apptek_url + clip['media'],
        }
        for clip in data['response']['docs']
    ]
    '''

    ''' If we just want link to IDENTV'''
    video_urls = [apptek_url + clip['media'] for clip in data['response']['docs']]
    num_vidoes = data['response']['numFound']
    return num_vidoes, payload
