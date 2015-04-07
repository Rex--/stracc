import flask
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import database
import cig
import os

app = flask.Flask(__name__)


def recordBS(bloodsugar, timeOfDay, date='today'):
    db.addData(date, timeOfDay, 'bloodsugar', bloodsugar)
    cig.updateChart(radarChart, db, charttogen='today')
    cig.updateChart(lineChart, db, charttogen='thisweek')
    cig.updateChart(lineChart, db, charttogen='thismonth')

def recordShot(shot, timeOfDay, date='today'):
    db.addData(date, timeOfDay, 'shot', shot)
    cig.updateChart(radarChart, db, charttogen='today')
    cig.updateChart(lineChart, db, charttogen='thisweek')
    cig.updateChart(lineChart, db, charttogen='thismonth')

def delData(time, date, dtype):
    db.removeData(date, time, dtype)
    cig.updateChart(lineChart, db, charttogen='all')


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
        timeOfDay = req['timeofday']
        date = req['date']
    except KeyError as err:
        return flask.json.jsonify(error = "Bad request"), 400
    recordBS(bS, timeOfDay, date)
    return flask.json.jsonify(success="true"), 200

# Gets multiple blood sugar test and adds each one to the db.
@app.route('/test/multiple', methods=['POST'])
def postMultipleBloodSugar():
    try:
        req = flask.request.get_json()
        sugars = req['bloodsugars']
        timesOfDay = req['timesofday']
        dates = req['dates']
    except KeyError:
        return flask.json.jsonify(error = 'Bad request'), 400

    for i in range(len(sugars)):
        recordBS(sugars[i], timesOfDay[i], dates[i])
    return flask.json.jsonify(success = 'true'), 200

@app.route('/test/remove', methods=['POST'])
def removeBloodsugar():
    try:
        req = flask.request.get_json()
        timeOfDay = req['timeofday']
        date = req['date']
    except KeyError:
        return flask.json.jsonify(error='Bad Request'), 400
    delData(timeOfDay, date, 'bloodsugar')
    return flask.json.jsonify(success='true'), 200

# Gets a shot and adds it to the database
@app.route('/shot', methods=['POST'])
def postShot():
    try:
        req = flask.request.get_json()
        shot = req['shot']
        timeOfDay = req['timeofday']
        date = req['date']
    except KeyError:
        return flask.json.jsonify(error = 'Bad Request'), 400
    recordShot(shot, timeOfDay, date)
    return flask.json.jsonify(success='true'), 200

@app.route('/shot/multiple', methods=['POST'])
def postMultipleShot():
    try:
        req = flask.request.get_json()
        shots = req['shots']
        timesOfDay = req['timesofday']
        dates = req['dates']
    except KeyError:
        return flask.json.jsonify(error='Bad Request'), 400

    for i in range(len(shots)):
        recordShot(shots[i], timesOfDay[i], dates[i])
    return flask.json.jsonify(success='true'), 200

@app.route('/shot/remove', methods=['POST'])
def removeShot():
    try:
        req = flask.request.get_json()
        timeOfDay = req['timeofday']
        date = req['date']
    except KeyError:
        return flask.json.jsonify(error='Bad Request'), 400
    return delData(timeOfDay, date, 'shot')


# Fucking browsers cant use favicons right >:|
@app.route('/favicon.ico')
def faviconGet():
    favicon = open('web-assets/images/sugar.ico', 'rb')
    return favicon.read()

# Catch all for pages outside of web-assets/ or that dont exist.
@app.route('/<path:path>')
def catchAll(path):
    return fourOhFour()

if not os.path.exists('web-assets/chart-data'):
    os.mkdir('web-assets/chart-data')
    os.mkdir('web-assets/chart-data/today')
    os.mkdir('web-assets/chart-data/thisweek')
    os.mkdir('web-assets/chart-data/thismonth')

db = database.Database('db')
lineChart = cig.LineChart()
radarChart = cig.RadarChart()
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(3160)
print 'Listening on port: 3160...'
IOLoop.instance().start()
