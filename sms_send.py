import requests
import json
import mysql.connector

URL = 'http://www.way2sms.com/api/v1/sendCampaign'

sql2="select * from sms123"
mydb=mysql.connector.connect(host="localhost",user="root",passwd="123456",database="election")
mycursor=mydb.cursor()
mycursor.execute(sql2)
idsms=mycursor.fetchall()
idsms1=idsms[0][0]

sql="select * from details where id="+str(idsms1)
mycursor.execute(sql)
smss=mycursor.fetchall()
name1=smss[0][1]
vid1=smss[0][3]
addr1=smss[0][4]
mobno=smss[0][5]
msg=str(name1)+"\n"+str(vid1)+"\n"+str(addr1)+"\n"+str(mobno)


# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':"RRS99WUWR8O4PNT8RV757HI2X3STDAAG",
  'secret':"US5EVID8CXSH6F5H",
  'usetype':"stage",
  'phone': 8277332768,
  'message':msg,
  'senderid':9113234632
  }
  return requests.post(reqUrl, req_params)

# get response
response = sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'message-text' )
"""
  Note:-
    you must provide apikey, secretkey, usetype, mobile, senderid and message values
    and then requst to api
"""
# print response if you want
print(response.text)
#view rawpython_sendcampaign_post.py hosted with ❤ by GitHub