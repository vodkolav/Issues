from flask import Flask, request, jsonify, abort
import API 

app = Flask(__name__)

@app.route("/")
def hello():
    return """Welcome to issues. Here are some usage examples: <br>
    http://127.0.0.1:5000/GetIssueAtTime?Issue=163623&Time=186461716436622 <br>
    http://127.0.0.1:5000/GetIssueAtTime?Issue=133474&Time=186925578209167 <br>
    remember to use appropriate ip """

@app.route("/GetIssueAtTime")
def test():
    Issue = request.args['Issue']
    Time = request.args['Time']
    try:
        return jsonify(API.GetIssueAtTime(Issue, Time))
    except Exception as e:
        abort(404)
if __name__ == '__main__':
  app.run(host='0.0.0.0')

# Example requests:
#http://127.0.0.1:5000/GetIssueAtTime?Issue=163623&Time=186461716436622

#http://127.0.0.1:5000/GetIssueAtTime?Issue=133474&Time=186925578209167

