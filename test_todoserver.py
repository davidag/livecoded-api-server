# test_todoserver.py
# How to run these tests: python -m unittest test_todoserver.py

# import doctest # good for writing very simple tests...
import unittest
import json
from todoserver import app


class TestTodoserver(unittest.TestCase):
    # better be verbose with test names, you'll only type this once!
    def test_get_empty_list_of_tasks(self):
        client = app.test_client()
        resp = client.get("/tasks/")
        # Expected value first (consistency in all tests)
        self.assertEqual(200, resp.status_code)
        # resp.data is of type bytes in Py3
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual([], data)
