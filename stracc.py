import flask
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import database
import cinfogen
import os

app = flask.Flask(__name__)


def recordBS(bloodsugar, time='now', date='today'):
    db.addData(date, time, 'tests', bloodsugar)
    cinfogen.updateChart(chartInfoGen, db, charttogen='all')

def recordShot(shot, time='now', date='today'):
    db.addData(date, time, 'shots', shot)
    cinfogen.updateChart(chartInfoGen, db, charttogen='all')

def deleteBSfromDB(id):
    print 'Feature not implemented..(Yet!)'

def fourOhFour():
    image = open("web-assets/404.html", 'r')
    return image.read(), 404

# Root
#   Serves today.html.
@app.route('/')
def stracc():
    index = open('web-assets/today.html', 'r')
    return index.read()

# Serves the web-assets I need for drawing etc.
@app.route('/web-assets/<path:path>')
def webAssets(path):
    fpath = str(os.path.join('web-assets', path))
    try:
        asset = open(fpath, 'r')
    except IOError:
        return fourOhFour()
    return asset.read()


# Gets a bloodsugar test and adds it the the database
@app.route('/test', methods=['POST'])
def postBloodSugar():
    try:
        req = flask.request.get_json()
        bS = req['bloodsugar']
        time = req['time']
        date = req['date']
    except KeyError as err:
        return flask.json.jsonify(error = "Bad request"), 400
    recordBS(bS, time, date)
    return flask.json.jsonify(success="true"), 200

# Gets multiple blood sugar test and adds each one to the db.
@app.route('/test/multiple', methods=['POST'])
def postMultipleBloodSugar():
    try:
        req = flask.request.get_json()
        sugars = req['bloodsugars']
        times = req['times']
        dates = req['dates']
    except KeyError:
        return flask.json.jsonify(error = 'Bad request'), 400

    for i in range(len(sugars)):
        recordBS(sugars[i], times[i], dates[i])
    return flask.json.jsonify(success = 'true'), 200

# Gets a shot and adds it to the database
@app.route('/shot', methods=['POST'])
def postShot():
    try:
        req = flask.request.get_json()
        shot = req['shot']
        time = req['time']
        date = req['date']
    except KeyError:
        return flask.json.jsonify(error = 'Bad Request'), 400
    recordShot(shot, time, date)
    return flask.json.jsonify(success='true'), 200

@app.route('/shot/multiple', methods=['POST'])
def postMultipleShot():
    try:
        req = flask.request.get_json()
        shots = req['shots']
        times = req['times']
        dates = req['dates']
    except KeyError:
        return flask.json.jsonify(error='Bad Request'), 400

    for i in range(len(shots)):
        recordShot(shots[i], times[i], dates[i])
    return flask.json.jsonify(success='true'), 200

# Fucking browsers cant use favicons right >:|
@app.route('/favicon.ico')
def faviconGet():
    favicon = open('web-assets/images/sugar.ico', 'rb')
    return favicon.read()

# Catch all for pages outside of web-assets/ or that dont exist.
@app.route('/<path:path>')
def catchAll(path):
    return fourOhFour()

db = database.Database('db')
chartInfoGen = cinfogen.LineChart()
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(3160)
print 'Listening on port: 3160...'
IOLoop.instance().start()
