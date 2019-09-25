# todoserver/app.py

import json

# As you import more and more things, this () form starts being really useful,
# specially for diffs with multiple developers working.
from flask import (
    Flask,
    make_response,
    request,
)

from .store import TaskStore


class TodoserverApp(Flask):
    def __init__(self, name):
        self.store = TaskStore()
        # In Py2, super(TodoserverApp, self)
        super().__init__(name)

    def erase_all_test_data(self):
        assert self.testing
        # This breaks a bit encapsulation but at least this method is cohesive
        self.store.tasks.clear()

app = TodoserverApp(__name__)


@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = app.store.get_all_tasks()
    return make_response(json.dumps(tasks), 200)


@app.route("/tasks/", methods=["POST"])
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


@app.route("/tasks/<int:task_id>/")
def task_details(task_id):
    task_info = app.store.get_task_details(task_id)
    return json.dumps(task_info)
