import pymysql
from flask import Flask
from flask import request
from flask.json import jsonify
import json
import requests
import http.client
from flask import Response
import re

app=Flask(__name__)
@app.route('/tharun',methods=['POST'])
def name():

   action = request.get_json()['queryResult']['action']
   db = pymysql.connect("localhost", "root", "root", "game_finder")
   cursor = db.cursor()
   if action=="signup":
         user_id= request.get_json()['originalRequest']['data']['sender']['id']
         name=request.get_json()['queryResult']['parameters']['name']
         email=request.get_json()['queryResult']['parameters']['email']
         phone_num=request.get_json()['queryResult']['parameters']['mobile']
         password=request.get_json()['queryResult']['parameters']['password']
         sql = "INSERT INTO game_finder(id,name,email,password,phone,booking_status,partner)\
                                VALUES ('%s','%s','%s','%s','%s',%d ,'%s')" % \
               (user_id, name, email,password, phone_num,0,'N')
         sql1="INSERT INTO game_finder1(id,name,email,password,phone,booking_status,partner)\
                                VALUES ('%s','%s','%s','%s','%s',%d,'%s')" % \
               (user_id, name, email,password, phone_num,0,'N')
         try:
             # Execute the SQL command
             cursor.execute(sql)
             cursor.execute(sql1)
             # Commit your changes in the database
             db.commit()
             s1 = { "messages": [
               {
                 "type": 0,
                 "platform": "facebook",
                 "speech": "sucessfully signed up"
               }

              ],
                "messages": [
                 {
                     "platform": "facebook",
                     "replies": [
                         "continue",
                         "exit"


                     ],
                     "title": "choose one",
                     "type": 2
                 }
               ]
               }
             return Response(json.dumps(s1), mimetype='application/json')
         except:
             db.rollback()
             s2={ "messages": [
               {
                 "type": 0,
                 "platform": "facebook",
                 "speech": "sorry error occured"
               }

              ],
                 "messages": [
                     {
                         "platform": "facebook",
                         "replies": [

                             "exit",
                             "signup again"

                         ],
                         "title": "choose one",
                         "type": 2
                     }
                 ]
             }
             return Response(json.dumps(s2), mimetype='application/json')




         db.close()

   if action=="signingin":
       email = request.get_json()['queryResult']['parameters']['email']
       password=request.get_json()['queryResult']['parameters']['password']

       sql="select password from game_finder where email='%s'"%email
       cursor.execute(sql)
       result = cursor.fetchone()


       if result[0]==password:
           s3 = {"messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "sucessfully signed in"
               }

           ],
               "messages": [
                   {
                       "platform": "facebook",
                       "replies": [
                           "continue",
                           "exit"

                       ],
                       "title": "choose one",
                       "type": 2
                   }
               ]
           }
           return Response(json.dumps(s3), mimetype='application/json')
       else:
           s4 = {"messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "sorry error occured"
               }

           ],
               "messages": [
                   {
                       "platform": "facebook",
                       "replies": [
                           "retry to sign in",
                           "exit"

                       ],
                       "title": "choose one",
                       "type": 2
                   }
               ]
           }
           return Response(json.dumps(s4), mimetype='application/json')
       db.close()




   if action=="player_available":
       game=request.get_json()['queryResult']['queryText']
       email=request.get_json()['queryResult']['outputContexts'][0]['parameters']['email']
       query = "update game_finder set sport='%s' where email= '%s'" % (game, email)
       query1 = "update game_finder1 set sport='%s' where email='%s'" % (game, email)
       try:
           # Execute the SQL command
           cursor.execute(query)
           cursor.execute(query1)
           # Commit your changes in the database
           db.commit()
       except:
           db.rollback()

           query3 = "select name from game_finder1 where sport='%s' and booking_status=%d" % (game, 0)
       cursor.execute(query3)
       partners=cursor.fetchall()
       db.close()
       if len(partners)<2:
           msg = {
               "messages": [
                   {
                       "type": 0,
                       "platform": "facebook",
                       "speech": "sorry their is no player available for you now"
                   },
                   {
                       "type": 2,
                       "platform": "facebook",
                       "title": "Please Choose Below",
                       "replies": [
                           "exit",

                       ]
                   }
               ]
           }
           return Response(json.dumps(msg), mimetype='application/json')
       else:
           s10 = {
               "messages": [
                   {
                       "type": 2,
                       "platform": "facebook",
                       "title": "choose a player from below",
                       "replies": []
                   }]
           }
           players_list=[]
           for i in partners:
               players_list.append(i)

           s10['messages'][0]['replies']=players_list

           return Response(json.dumps(s10), mimetype='application/json')

   if action=='booked_player':
       user_id = request.get_json()['originalRequest']['data']['sender']['id']
       query4='select email from game_finder where id=%d'%user_id
       cursor.execute(query4)
       mail=cursor.fetchone()
       your_email=mail[0]

       partner_name=request.get_json()['queryResult']['parameters']['partner_fix']
       p_mail_query="select mail from game_finder where name='%s'"%(partner_name)
       cursor.execute(p_mail_query)
       res=cursor.fetchall()
       p_mail=res[0]

       query5="update game_finder set partner='%s' where email='%s'"%(p_mail,your_email)
       query6 = "update game_finder set partner='%s' where email='%s'" % (your_email, p_mail)
       query7 = "update game_finder1 set partner='%s' where email='%s'" % (p_mail, your_email)
       query8 = "update game_finder1 set partner='%s' where email='%s'" % (your_email, p_mail)
       try:
           cursor.execute(query5)
           cursor.execute(query6)
           cursor.excecute(query7)
           cursor.execute(query8)
           db.commit()

           query9="select phone from game_finder where email='%s'"%p_mail

           cursor.execute(query9)
           phone=cursor.fetchall()
           p_phone=phone[0]
           details = {  "messages": [
                   {
                       "type": 0,
                       "platform": "facebook",
                       "speech": "your paartner details are"
                   },
           {
               "type": 0,
               "platform": "facebook",
               "speech": []
            }

            ]
           }
           details_list=[]

           details_list.append(p_mail)
           details_list.append(p_phone)
           details['messages'][1]['speech']=details_list

           return Response(json.dumps(details), mimetype='application/json')
       except:
           db.rollback()

           s90={"messages": [
               {
                   "type": 0,
                   "platform": "facebook",
                   "speech": "sorry error occured"
               }

           ]
           }
           return Response(json.dumps(s90), mimetype='application/json')

if __name__=="__main__":
    app.run(host = '0.0.0.0' ,debug=True,port=1010)
