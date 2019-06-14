import requests
from dateutil.parser import parse
import logging

def get_videos(data):

    base_url = "http://mm.apptek.com:8983/solr/media/select"
    media_url = "http://mm.apptek.com/media"
    apptek_url = "http://mm.apptek.com/tv/watch?id="

    channel = data['channel']
    language = 'ar'
    query = data['query']
    results_limit = 100000
    start_date = data['start_date']
    end_date = data['end_date']

    q = 'source:' + channel + ' AND ' + 'lang:' + language + ' AND ' + query

    payload = {
        'q' : q,
        'wt' : 'json',
        'sort' : 'start_dt desc',
        'rows' : results_limit,
        #'fl' : 'start_dt,end_dt,duration,media,' + 'seg_' + language,
        'fl' : 'start_dt,end_dt,duration,media,',
        'fq' : 'start_dt:[' + start_date + ' TO ' + end_date + ']',
    }

    r = requests.get(base_url, params = payload)
    data = r.json()

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
    return num_vidoes, video_urls
