from flask import Flask, request, jsonify
from celery.result import AsyncResult
import json
from worker import countWords, celery_app


app = Flask(__name__)

@app.route('/count', methods=['POST'])
def count():
    data = request.get_json()
    text = data.get("text")

    if len(text.split(" ")) < 2 or len(text.split(" ")) > 10:
        return jsonify({"error" : "incorrect input"}), 400

    result = countWords.delay(text)
    return json.dumps({"id": result.id}), 200

@app.route('/status/<id>')
def getResultFromID(id):
    try:
        res = AsyncResult(id, app=celery_app)
    except:
        return json.dumps({"error":"invalid ID"}), 400
    if res.status == "SUCCESS":
        return json.dumps({"Result" : res.status}), 200
    else:
        return json.dumps({"Result" : res.status}), 400


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=5050)