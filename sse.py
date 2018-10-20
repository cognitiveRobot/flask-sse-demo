"""Example of using server-sent events with Flask using gevent.

This can be run as-is using gevent's built-in WSGI server, or you can
run it with gunicorn as follows::

  gunicorn -b 127.0.0.1:5000 -k gevent sse:app

If testing connections with a single browser, keep in mind that the
browser may have a setting to limit the number of persistent
connections per server. For example, in Firefox, there is a
``network.http.max-persistent-connections-per-server`` setting which
defaults to 6 (at least on my browser).

"""

import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
from numpy import random
from flask import Flask, json, Response, render_template
from queue import Queue
import threading

app = Flask(__name__)
app.debug = True

q = Queue()

x = 0

temp_c = 0
# Logging temp data
def log_temp(name):
    print("Starting " + name)
    while True:
        global temp_c
        temp_c = temp_c + 1
        q.put(temp_c)
        print("temp added: ", temp_c)
        gevent.sleep(0.5)

humidity_c = 0
# Logging humidity data
def log_humidity(name):
    print("Starting " + name)
    while True:
        global humidity_c
        humidity_c = humidity_c + 1000
        q.put(humidity_c)
        print("humidity added: ", humidity_c)
        gevent.sleep(0.5)

def event_stream():
    print("Starting streaming")
    while True:
        result = q.get()
        print(result)
        yield 'data: %s\n\n' % str(result)
        gevent.sleep(.5)

@app.route('/')
def index():
    print("Index requested")
    return render_template('index.html')

@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    # gevent.sleep(1)
    print("stream requested/posted")
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    # Create two threads as follows
    try:
       th1 = threading.Thread(target=log_temp, args=("temp_logger",))
       th2 = threading.Thread(target=log_humidity, args=("humidity_logger",))
       th1.start()
       th2.start()
       print ("Thread(s) started..")
    except:
        print ("Error: unable to start thread")
    else:
        WSGIServer(('', 5000), app).serve_forever()
