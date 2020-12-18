from flask import Flask
from flask_pymongo import PyMongo, MongoClient
from bson.json_util import dumps
from flask import jsonify,request

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017"
mongo = PyMongo(app, uri="mongodb://localhost:27017/Users")

logger = PyMongo(app, uri="mongodb://localhost:27017/RevisionLog")
localDb=PyMongo(app, uri="mongodb://localhost:27017/local")
#client = MongoClient("mongodb+srv://user:<password>@example-xkfzv.mongodb.net/test?retryWrites=true")

Create_Action = 1

@app.route('/currentLogged')
def add_user():
    if Create_Action :
        revisedLogs = localDb.db.startup_log.find()
        response = dumps(revisedLogs)
        x = response.split(": ")
        userName = x[1].split(", ")[0]
        hostName = x[2].split(", ")[0]
        startTime= x[5].split(", ")[0]
        log_User_id=logger.db.revisionLog.insert({
            'ChangedByUser' :userName,
            'ChangedByHost': hostName,
             'ChangedOn':startTime,
               'Changes': "ChangesMade Needs to have a replica set."
        })
        resp = jsonify("Logs added success")
        resp.status_code = 200
        return resp
    else:
         return not_found()

# @app.route('/logs')
# def printChanges():
#     change_stream = client.changestream.collection.watch([{
#         '$match': {
#         'operationType': { '$in': ['insert'] }
#             }
#         }])
#     for change in change_stream:
#         print(dumps(change))
#     print('')
#     return dumps(change)

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp=jsonify(message)
    resp.status_code =404
    return resp
if __name__== "__main__":
    app.run(debug=True)