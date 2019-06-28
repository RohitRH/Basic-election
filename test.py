from flask import Flask, render_template,url_for,request,session,redirect, make_response
from datetime import datetime
import time,os
import mysql.connector
import alerts
import final
import dataset,predictor
import trainer
app=Flask(__name__)
app.config['SECRET_KEY']=b'N\x83Y\x99\x04\xc9\xcfI\xb7\xfc\xce\xd1\xcf\x01\xa8\xccr\xbb&\x1b\x11\xac\xc7V'
app.config['MAX_CONTENT_PATH']=1024
USER = 'admin'
PASS = 'admin'




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = request.form['user']
        pw = request.form['pw']
        if (user == USER and pw == PASS):
            return redirect('/admin')
        return render_template('login.html',msg="Incorrect Username or Password")

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'GET' :
        return render_template('admin.html',loggedin = True)



@app.route('/datagen', methods=['GET','POST'])
def datagen():
    if request.method == 'GET' :
        return render_template('datagen.html', loggedin = True )
    if request.method == 'POST' :
        Id = request.form['Id']
        name = request.form['name']
        address = request.form['address']
        mobno = request.form['mobile number']
        print(Id,name)
        #function call
        predictor.hello(Id,name,address,mobno)
        os.system('python dataset.py')
        n1,dupli=alerts.alrts()
        print(n1)
        msg = str(n1) + " records inserted"

        print(dupli)
        if(dupli[0][0]==1):
            msg = "Dataset Already Exists"
            #send alert as DATASET ALREADY EXISTS

        #send alert as n1 records inserted
        os.system('python trainer.py')
       # dataset.generate(Id,name)
        #trainer.trainer()
        #os.system('python trainer.py')
        return render_template('admin.html',dupli_msg=msg,loggedin=True)

@app.route('/logout', methods=['GET','POST'])
def logout():
    return redirect('/index')

@app.route('/start', methods=['GET','POST'])
def start():
    #final.getface(1)
    os.system('python final.py')
    return redirect('admin')

@app.route('/show fraudulents', methods=['GET','POST'])
def example():
    gt=alerts.get_table()
    if request.method == 'GET' :
        return render_template('example.html',value=gt,loggedin=True)

@app.errorhandler(404)
def not_found(e):
    return redirect("/index")

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')