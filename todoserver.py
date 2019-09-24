# todoserver.py

from flask import Flask, make_response

app = Flask(__name__)

@app.route("/tasks/")
def get_all_tasks():
    return make_response("[]", 200)

if __name__ == "__main__":
    app.run()
