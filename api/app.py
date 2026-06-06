from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os
import time

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/tododb")
client = MongoClient(MONGO_URI)
db = client.tododb
todos = db.todos

# ── Métriques Prometheus ──
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)
TODO_COUNT = Counter(
    'todos_created_total',
    'Total todos created'
)


@app.before_request
def start_timer():
    request._start_time = time.time()


@app.after_request
def record_metrics(response):
    if request.path != '/metrics':
        duration = time.time() - request._start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.path
        ).observe(duration)
    return response


def serialize(todo):
    return {
        "_id": str(todo["_id"]),
        "title": todo["title"],
        "done": todo.get("done", False)
    }


@app.route("/metrics")
def metrics():
    """Endpoint pour Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "ok", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 500


@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = list(todos.find())
    return jsonify([serialize(t) for t in all_todos])


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "title requis"}), 400
    result = todos.insert_one({"title": data["title"], "done": False})
    todo = todos.find_one({"_id": result.inserted_id})
    TODO_COUNT.inc()
    return jsonify(serialize(todo)), 201


@app.route("/todos/<id>", methods=["PUT"])
def toggle_todo(id):
    todo = todos.find_one({"_id": ObjectId(id)})
    if not todo:
        return jsonify({"error": "non trouve"}), 404
    todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": not todo["done"]}})
    updated = todos.find_one({"_id": ObjectId(id)})
    return jsonify(serialize(updated))


@app.route("/todos/<id>", methods=["DELETE"])
def delete_todo(id):
    result = todos.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "non trouve"}), 404
    return jsonify({"message": "supprime"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
