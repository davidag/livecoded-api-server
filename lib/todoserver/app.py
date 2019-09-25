# todoserver/app.py

from flask import Flask, make_response, request
import json

app = Flask(__name__)

# Don't require a db yet, as it's not the focus of the test we're creating
MEMORY = {}

@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = [
        {
            "id": task_id,
            "summary": task["summary"]
        }
        for task_id, task in MEMORY.items()
    ]
    return make_response(json.dumps(tasks), 200)


@app.route("/tasks/", methods=["POST"])
def create_task():
    # request will always contain info about the current request
    # we're not requiring the content-type header as it's not a requirement yet
    payload = request.get_json(force=True)
    try:
        # !!! Non-thread safe !!! Never do this in production !!!
        task_id = 1 + max(MEMORY.keys())
    except ValueError:
        task_id = 1
    MEMORY[task_id] = {
        "summary": payload["summary"],
        "description": payload["description"],
    }
    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)


@app.route("/tasks/<int:task_id>/")
def task_details(task_id):
    task_info = MEMORY[task_id].copy()
    task_info["id"] = task_id
    return json.dumps(task_info)
