import requests
from dateutil.parser import parse
import logging
import re

def get_videos(data):

    base_url = "http://mm.apptek.com:8983/solr/media/select" # URL for sending the GET request
    media_url = "http://mm.apptek.com/media" # URL prefix that sends us straight to the mp4
    apptek_url = "http://mm.apptek.com/tv/watch?id=" # URL prefix that sends us to the video in the UI
    time_concat = ":00Z" # Solr wants datetime to end with this

    channel = data['channel'] # Channel parameter as specified by user
    language = 'ar' # Language code to be passed in GET request
    results_limit = data['limit'] # limit the number of rows we get in response from IdenTV (specified by user)
    start_date = data['start_date'] + time_concat # datetime string to be passed to GET request
    end_date = data['end_date'] + time_concat # datetime string to be passed to GET request

    query = data['query'] # query input by user
    query = query.split('\r\n') # query takes multiline form, place each segment as item in array

    # create a pattern that will be used to identify which words were actually found
    search_tokens = ' '.join(query) # join all the lines with a space
    search_tokens = [x for x in search_tokens.split('"') if x and not x.isspace()] # remove the double quotes everywhere
    search_tokens = '|'.join(search_tokens) # Place an "OR" operator between each term
    search_tokens = search_tokens.replace("*", r"\w*") # change the * to regex compliant \w*
    pattern = re.compile(search_tokens)

    # loop through the user input line by line and build the SOLR query to be used
    for i, line in enumerate(query):
        line = [x for x in line.split('"') if x and not x.isspace()]
        for x, phrase in enumerate(line):
            if ' ' in phrase:
                line[x] = phrase.replace(" ", " AND ")
        line = ["(" + x + ")" for x in line]
        line = " OR ".join(line)
        query[i] = "seg_ar:(" + line + ")"
    query = " AND ".join(query) #<----resultant query to be passed to Solr API

    # search component of GET parameter
    q = 'source:' + channel + ' AND ' + 'lang:' + language + ' AND ' + query

    payload = {
        'q' : q,
        'wt' : 'json', # output format of the API call
        'sort' : 'start_dt desc', # sort the Solr results most recent TV clip first
        'rows' : results_limit, # limits the result displayed but doesn't limit the total count
        'fl' : 'start_dt,media,seg_ar', #filter to only these fields in the result.
        # seg_ar gives the actual transcription output, media gives the TV clip ID, start_dt gives the start time stamp of the media clip
        'fq' : 'start_dt:[' + start_date + ' TO ' + end_date + ']', # filter by date
    }

    r = requests.get(base_url, params = payload)
    data = r.json()

    payload = [
        {
            'video_url' : apptek_url + clip['media'],
            'tokens' : pattern.findall(' '.join(clip['seg_ar'])),
            # 'mp4' : "/".join((media_url, channel, parse(clip['start_dt']).date().strftime('%Y/%m/%d'), clip['media'] + '.mp4')),
            # Above previously used to access the mp4 file directly instead of linking to the IdenTV UI
        }
        for clip in data['response']['docs']
    ]

    num_vidoes = data['response']['numFound']

    return num_vidoes, payload
