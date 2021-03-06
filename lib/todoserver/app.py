# todoserver/app.py

import json
from functools import wraps

# As you import more and more things, this () form starts being really useful,
# specially for diffs with multiple developers working.
from flask import (
    Flask,
    make_response,
    request,
)

from .store import TaskStore, BadSummaryError


class TodoserverApp(Flask):
    def init_db(self, engine_spec):
        self.store = TaskStore(engine_spec)

    def erase_all_test_data(self):
        assert self.testing
        # This breaks a bit encapsulation but at least this method is cohesive
        self.store._delete_all_tasks()

app = TodoserverApp(__name__)

def validate_summary(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except BadSummaryError:
            result = {"error": "Summary must be under 120 chars, without newlines"}
            return make_response(json.dumps(result), 400)
    return wrapper


@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = app.store.get_all_tasks()
    return make_response(json.dumps(tasks), 200)


@app.route("/tasks/", methods=["POST"])
@validate_summary
def create_task():
    # request will always contain info about the current request
    # we're not requiring the content-type header as it's not a requirement yet
    payload = request.get_json(force=True)
    # we explicitly use keyword args as these can be potentially confused
    task_id = app.store.create_task(
        summary = payload["summary"],
        description = payload["description"],
    )
    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)


@app.route("/tasks/<int:task_id>/", methods=["PUT"])
@validate_summary
def modify_task(task_id):
    payload = request.get_json(force=True)
    modified = app.store.modify_task(
        task_id,
        payload["summary"],
        payload["description"]
    )
    if modified:
        return ""
    else:
        return make_response("", 404)


@app.route("/tasks/<int:task_id>/")
def task_details(task_id):
    task_info = app.store.get_task_details(task_id)
    if task_info is None:
        return make_response("", 404)
    return json.dumps(task_info)


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    deleted = app.store.delete_task(task_id)
    if deleted:
        return ""
    else:
        return make_response("", 404)
