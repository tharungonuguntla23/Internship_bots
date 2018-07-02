
import pymysql
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

   db = pymysql.connect("localhost", "root", "root", "details")
   cursor = db.cursor()
   action=request.get_json()['queryResult']['action']
   if action=="search":
       id = request.get_json()['queryResult']['parameters']['number']


       sql = "SELECT * FROM emp_details\
            where id=%d"%(id)


       cursor.execute(sql)
       result=cursor.fetchone()

       if result==None:
           s1 = {
               "messages": [
                   {
                       "type": 0,
                       "platform": "facebook",
                       "speech": "sorry their is no user with this id"
                   },
                   {
                       "type": 2,
                       "platform": "facebook",
                       "title": "Please Choose Below",
                       "replies": [
                           "insert details",

                       ]
                   }
               ]
           }
           return Response(json.dumps(s1), mimetype='application/json')


       else:
            return Response(json.dumps(result), mimetype='application/json')


       db.close()

   elif action=="inserting":
       insert_id=request.get_json()['queryResult']['parameters']['eid']
       insert_name=request.get_json()['queryResult']['parameters']['ename']
       insert_des=request.get_json()['queryResult']['parameters']['edes']
       sql = "INSERT INTO emp_details(id,name,designation) \
          VALUES ('%d','%s','%s' )" % \
             (insert_id,insert_name,insert_des)
       try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           db.commit()

           s3= {  "messages": [
                   {
                       "type": 0,
                       "platform": "facebook",
                       "speech": "data inserted sucesfully"
                   }
               ]
            }
           return Response(json.dumps(s3), mimetype='application/json')
       except:
           # Rollback in case there is any error
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



if __name__=="__main__":
    app.run(host = '0.0.0.0' ,debug=True,port=1010)