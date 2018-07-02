import pymysql
from flask import Flask
from flask import request
from flask.json import jsonify
import json
import requests
import http.client
from flask import Response
id=1
app=Flask(__name__)
@app.route('/tharun',methods=['POST'])
def name():

   action = request.get_json()['queryResult']['action']
   psid = request.get_json()['originalRequest']['data']['sender']['id']
   page_acess_token = "EAADVJ15gYMMBANZAbn5pdOoEUyTuVRmrt8PGzkrBFjVCZAuk4ijZCLmZC5sRAPm1Dun1jQrCWDcUy2de6Wy9ZARIsd8BYKOl1pOZAIWx949bYboW8TgS1oGMdg6J7JORoYptXtlNADERutmHMj5dUjOZAja3zsie6H57aQl7ivCyf7krpd4bSI7"
   url = "https://graph.facebook.com/v2.6/" + psid + "?access_token=" + page_acess_token

   details = requests.get(url)
   user_details = json.loads(details)
   fir_name = user_details['first_name']
   las_name = user_details['last_name']
   u_name = fir_name + las_name
   if action =="welcome":
       s1 = {
           "messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "hello" + u_name
               }
           ]
       }
       return Response(json.dumps(s1), mimetype='application/json')

   elif action=="insert":
       db = pymysql.connect("localhost", "root", "root", "user_location_details")
       cursor = db.cursor()
       latitude = request.get_json()['originalDetectIntentRequest']['payload']['data']['lat']
       longitude = request.get_json()['originalDetectIntentRequest']['payload']['data']['long']
       sql = "INSERT INTO user_location \
                       VALUES ('%d','%s','%s','%s' )" % \
             (++id, u_name, latitude, longitude)


       try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           db.commit()
           s3 = {"messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "data inserted sucesfully"
               }
           ]
           }
           return Response(json.dumps(s3), mimetype='application/json')
       except:
           db.rollback()
           s4 = {"messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "sorry data is not inserted because of some problems"
               }
           ]
           }
           return Response(json.dumps(s4), mimetype='application/json')
       db.close()

   elif action=="attachments":
       img=request.get_json();
       img_url=img['originalRequest']['data']['message']['attachments']['payload']['url']
       db = pymysql.connect("localhost", "root", "root", "user_location_details")
       cursor = db.cursor()
       sql = "INSERT INTO user_location(img_url) \
                              VALUES ('%s' )" % (img_url)

       try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           db.commit()
       except:
           db.rollback()
           s10 = {"messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "sorry data is not inserted because of some problems"
               }
           ]
           }
           return Response(json.dumps(s10), mimetype='application/json')
       db.close()


       sk={"messages": [
           {
               "imageUrl": "http://urltoimage.com",
               "platform": "facebook",
               "type": 3
           }
       ],
           "messages": [
               {
                   "platform": "facebook",
                   "replies": [
                       "continue",
                       "bye",

                   ],
                   "title": "choose one",
                   "type": 2
               }
           ]
       }
       return Response(json.dumps(sk), mimetype='application/json')

if __name__=="__main__":
    app.run(host = '0.0.0.0' ,debug=True,port=1010)



