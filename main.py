#use this command to run
'''flask run -h 0.0.0.0 -p 8080'''
from flask import Flask, request, redirect, render_template
from identv_api import get_videos

app = Flask(__name__)

@app.route('/')
def hello():
    return 'You love IIP'

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
        'limit' : request.form['limit'],
    }
    num, payload = get_videos(submit_data)

    return render_template('output.html', num=num, payload=payload)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
