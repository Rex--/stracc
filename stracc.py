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
    saveDbTabletoJson(db, 'bloodsugars')

def saveDbTabletoJson(db, table):
    dbtable = db[table]
    dataset.freeze(dbtable, format="json", filename="web-assets/bloodsugars.json")

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
    print "Bloodsugar: ", bS
    print "Time: ", time
    print "Meds: ", med
    recordBStoDB(bS, time, med)
    return flask.json.jsonify(success="true"), 200

if not os.path.exists('db'):
    os.mkdir('db')

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(3160)
IOLoop.instance().start()
