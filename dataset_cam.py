import cv2
import mysql.connector
import final

def generate():
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="123456",database="election")
    mycursor=mydb.cursor()

    sql7="update alerts set dupli=0"
    mycursor.execute(sql7)
    mydb.commit()

    sql10="update records set n=0"
    mycursor.execute(sql10)
    mydb.commit()

    sql3="select first from valid"
    mycursor.execute(sql3)
    fid=mycursor.fetchone()
    if(fid[0]!=0):
        dupli=final.duplidata()
        print(dupli)
        if(dupli=="user"):
            sql8="update alerts set dupli=1"
            mycursor.execute(sql8)
            mydb.commit()
            print("dataset already exists ")
            exit(0)

    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    sql6="select * from hello"
    mycursor.execute(sql6)
    hello=mycursor.fetchall()
    vid=hello[0][0]
    name=hello[0][1]
    address=hello[0][2]
    mobile_no=hello[0][3]
    sql1="select vid from details where vid="+str(vid)
    mycursor.execute(sql1)
    pid=mycursor.fetchall()
    exists=0
    for row in pid:
        exists=1
    if(exists==1):
        print("record already exists try another")
        exit(0)
    sql4="update valid set first=1"
    id=1
    if(fid[0]!=0):
        sql5="select id from details order by id desc"
        mycursor.execute(sql5)
        rid=mycursor.fetchall()
        id=rid[0][0]+1
    sql="insert into details(id,name,times,vid,address,mobile_no) values(%s,%s,%s,%s,%s,%s)"
    a=0
    val=(id,name,a,vid,address,mobile_no)
    count=0
    while True:
        ret,img=cam.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray,1.3,5)
        if faces is():
            print("face not found")
        for(x,y,w,h) in faces:
            count=count+1
            cv2.imwrite("image_dataset/user."+str(id)+"."+str(count)+"."+"jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.waitKey(1)
        cv2.imshow("face",img)
        if(count>50):
            break
    cam.release()
    cv2.destroyAllWindows()
    mycursor.execute(sql,val)
    n=mycursor.rowcount
    mycursor.execute(sql4)
    mydb.commit()
    sql9="update records set n=%s where n=%s"
    v=(n,0)
    mycursor.execute(sql9,v)
    mydb.commit()
    print(n,"records inserted")
    mydb.close()

if __name__=="__main__":
    generate()