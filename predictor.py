import mysql.connector

def hello(i,n,a,m):
    sql="update hello set id=%s,name=%s,address=%s,mobile_no=%s"
    #sql1="update hello set name="
    val=(i,n,a,m)
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
    mycursor = mydb.cursor()
    mycursor.execute(sql,val)
    mydb.commit()
    #mycursor.execute(sql1)
    #mydb.commit()


