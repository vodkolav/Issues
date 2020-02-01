from flask import Flask, request, jsonify
import API 

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/GetIssueAtTime")
def test():
    Issue = request.args['Issue']
    Time = request.args['Time']
    return jsonify(API.GetIssueAtTime(Issue, Time))

if __name__ == '__main__':
  app.run()


#http://127.0.0.1:5000/GetIssueAtTime?Issue=163623&Time=186461716436622

#http://127.0.0.1:5000/GetIssueAtTime?Issue=133474&Time=186925578209167

