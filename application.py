import funtions as f
from flask import Flask, jsonify

application = Flask(__name__)
data = f.load_file('./heroes.csv')

@application.route("/")
def index():
    return jsonify(data)

@application.route("/<string:id>")
def heroe(id):
    # Return 404 if the hero id does not exist
    if id not in data:
        return jsonify({"error": "not found", "id": id}), 404
    return jsonify(data[id])

if __name__ == "__main__":
    application.run(port = 5000, debug = True)