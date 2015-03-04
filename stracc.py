import flask
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import dataset
import os

app = flask.Flask(__name__)


def recordBStoDB(bs, t, m="none"):
    db = dataset.connect("sqlite:///db/bloodsugars.db")
    table = db['bloodsugars']
    table.insert(dict(bloodsugar=bs, time=t, med=m))

def saveDbTabletoJson():
    db = dataset.connect('sqlite:///db/bloodsugars.db')
    dbtable = db['bloodsugars']
    dataset.freeze(dbtable, format="json", filename="web-assets/bloodsugars.json")

def deleteBSfromDB(id):
    db = dataset.connect('sqlite:///db/bloodsugars.db')
    dbtable = db['bloodsugars']
    if id != 'all':
        dbtable.delete(id=id)
    else:
        dbtable.delete()

# Main bloodsugar graph
#   Serves chart.js chart.
@app.route('/')
def stracc():
    index = open('web-assets/index.html', 'r')
    return index.read()

# Serves the web-assets I need for drawing etc.
@app.route('/web-assets/<path:path>')
def webAssets(path):
    fpath = str(os.path.join('web-assets', path))
    asset = open(fpath, 'r')
    return asset.read()

# Gets a bloodsugar test and adds it the the database
@app.route('/test', methods=['POST'])
def postBloodSugar():
    try:
        req = flask.request.get_json()
        bS = req['bloodsugar']
        time = req['time']
        med = req['med']
    except KeyError as err:
        return flask.json.jsonify(error = "Bad request"), 400
    recordBStoDB(bS, time, med)
    saveDbTabletoJson()
    return flask.json.jsonify(success="true"), 200

# Gets multiple blood sugar test and adds each one to the db.
@app.route('/test/multiple', methods=['POST'])
def postMultipleBloodSugar():
    try:
        req = flask.request.get_json()
        sugars = req['bloodsugars']
        times = req['times']
        meds = req['meds']
    except KeyError:
        return flask.json.jsonify(error = 'Bad request'), 400

    for i in range(len(sugars)):
        recordBStoDB(sugars[i], times[i], meds[i])
    saveDbTabletoJson()
    return flask.json.jsonify(success = 'true'), 200

# Accepts a json db and replaces it with the current one.
@app.route('/test/updatedb', methods=['POST'])
def updateDB():
    try:
        req = flask.request.get_json()
        results = req['results']
    except KeyError:
        return flask.json.jsonify(error = 'Bad request'), 400

    deleteBSfromDB('all')

    for bs in results:
        recordBStoDB(bs['bloodsugar'], bs['time'], bs['med'])

    saveDbTabletoJson()
    return flask.json.jsonify(success = 'true'), 200

# Deletes the data entry with 'id'
@app.route('/test/delete', methods=['POST'])
def postTestDelete():
    try:
        req = flask.request.get_json()
        bsid = int(req['id'])
    except KeyError:
        return flask.json.jsonify(error = 'Bad request'), 400
    deleteBSfromDB(bsid)
    saveDbTabletoJson()
    return flask.json.jsonify(success='true'), 200

if not os.path.exists('db'):
    os.mkdir('db')

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(3160)
IOLoop.instance().start()
