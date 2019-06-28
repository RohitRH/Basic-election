import mysql.connector

def alrts():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
    mycursor = mydb.cursor()
    sql1 = "select * from records"
    sql = "select * from alerts"
    mycursor.execute(sql1)
    n = mycursor.fetchall()
    n1 = n[0][0]

    mycursor.execute(sql)
    dupli = mycursor.fetchall()
    return n1,dupli

def get_table():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="election")
    mycursor = mydb.cursor()
    mycursor.execute("select * from details where times>1")
    gt=mycursor.fetchall()
    return gt