from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

app = Flask(__name__)
from persistance import Sqlite
import json


PORT = 5000
DB = './tasks.db'

tasks = Sqlite(DB, 'tasks')

@app.route("/")
def index():
    return 'server running on 5000'

@app.route("/task", methods=['GET'])
def get_tasks():
    return jsonify(results = tasks.list())

@app.route("/task", methods=['POST'])
def create_task():
    data = request.get_json()
    tasks.add(data)
    return '', 201

@app.route("/task/<id>", methods=['GET'])
def get_task(id):
    result = tasks.get(id)
    if result:
        return jsonify(result)
    return make_response(jsonify(dict(error="Invalid task id")), 404)

@app.route("/task/<id>", methods=['DELETE'])
def delete_task(id):
    result = tasks.delete(id)
    if result:
        return '', 200
    return make_response(jsonify(dict(error="Invalid task id")), 404)

@app.route("/task/<id>", methods=['PUT'])
def update_task(id):
    data = request.get_json()
    result = tasks.update(id, data)
    if (result):
        return get_task(id)
    return make_response(jsonify(dict(error="Invalid task id")), 404)

if __name__ == '__main__':
    app.run()
