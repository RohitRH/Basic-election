import cv2
import mysql.connector
import urllib.request
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
#mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
#mycursor = mydb.cursor()

a=None
d=""

def getdetails(id):
    name=None
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
    mycursor = mydb.cursor()
    sql="select name from details where id="+str(id)
    mycursor.execute(sql)
    name=mycursor.fetchall()
    print(name)
    mydb.close()
    return name[0][0]



def find_dupli(id):
    mydb1 = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
    mycursor1 = mydb1.cursor()
    sql1="select times from details where id="+str(id)
    mycursor1.execute(sql1)
    times1=mycursor1.fetchall()
    print(times1[0][0])
    k=int(times1[0][0])+1
    print(k)
    sql2="update details set times="+str(k)+" where id="+str(id)
    mycursor1.execute(sql2)
    mydb1.commit()
    if(k>1):
        return "dupli"
    else:
        return "not dupli"



def getface(i):
    global d
    global a
    chk=0
    mydb1 = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
    mycursor1 = mydb1.cursor()
    sql1="insert into sms123(id,name) values(%s,%s)"
    sql2="delete from sms123"
    #cam = cv2.VideoCapture(0)
    url = "http://192.168.43.21:8080/shot.jpg"
    while True:
        #ret, im =cam.read()
        img = urllib.request.urlopen(url)
        # img = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        if faces is():
            print("face not found")
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            id1=Id
            name=getdetails(Id)
            print(conf)
            if(conf<65):
                Id=name
                if(a!=Id and i==1):
                    d=find_dupli(id1)
                    if(d=="dupli" and chk==0):
                        val=(id1,Id)
                        mycursor1.execute(sql1,val)
                        mydb1.commit()
                        os.system("python sms_send.py")
                        chk=1

                    a=Id
            else:
                Id="Unknown"
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            cv2.putText(im, str(Id), (x,y-40), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 3)
            if(Id!="Unknown"):
                cv2.putText(im, str(d), (x, y), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 3)
            print(d)
        cv2.imshow('im',im)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
    #cam.release()
    cv2.destroyAllWindows()
    mycursor1.execute(sql2)
    mydb1.commit()
    return Id


def duplidata():
    dupli=getface(0)
    if(dupli!="Unknown"):
        return "user"
    else:
        return "not user"


#def start():
#    getface(1)

if __name__=="__main__":
    getface(1)
