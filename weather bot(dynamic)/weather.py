from flask import Flask
from flask import request
from flask.json import jsonify
import json
import requests

import http.client
from flask import Response
app=Flask(__name__)
@app.route('/tharun',methods=['POST'])
def name():

    api_add = "http://api.openweathermap.org/data/2.5/weather?appid=7dbdda9541b2562eda52792b60f545ad&q="

    r=request.get_json()['queryResult']['parameters']['city']
    url = api_add + r

    data = requests.get(url).json()

    temp = data['weather'][0]['main']
    return Response(json.dumps(temp), mimetype='application/json')
if __name__=="__main__":
    app.run(host = '0.0.0.0' ,debug=True,port=8090)