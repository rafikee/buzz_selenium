#use this command to run
'''flask run -h 0.0.0.0 -p 8080'''
from flask import Flask, request, jsonify, redirect, render_template
from get_shares import get_shares
import requests
import os
from identv_api import get_videos
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'You love IIP'

@app.route('/iip', methods=['POST'])
def iip():
    if request.headers['token'] == os.environ.get('flask_key'):
        print("good job you have the right token")
        shares = get_shares(request.get_json())
        return jsonify(shares)
    else:
        print("intruder alert!")
        return "Leave me alone!"

@app.route('/cnn')
def comms():
    return redirect("https://storage.googleapis.com/identvclips/playme.mp4")

@app.route('/tv')
def input_form():
    return render_template('input_form.html')

@app.route('/tv', methods=['POST'])
def submit_query():
    submit_data = {
        'query' : request.form['query'],
        'start_date' : request.form['start_date'],
        'end_date' : request.form['end_date'],
        'channel' : request.form['channel'],
    }
    num, urls = get_videos(submit_data)

    return render_template('output.html', num=num, urls=urls)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
