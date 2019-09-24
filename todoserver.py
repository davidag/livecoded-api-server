# todoserver.py
import json
from flask import Flask, make_response, request

app = Flask(__name__)

# Don't require a db yet, as it's not the focus of the test we're creating
MEMORY = {}

@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    return make_response("[]", 200)


@app.route("/tasks/", methods=["POST"])
def create_task():
    # request will always contain info about the current request
    # we're not requiring the content-type header as it's not a requirement yet
    payload = request.get_json(force=True)
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


if __name__ == "__main__":
    app.run()
