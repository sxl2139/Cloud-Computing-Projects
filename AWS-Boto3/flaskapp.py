import os
from flask import Flask,request,render_template,make_response
app = Flask(__name__)
import time
from subprocess import call
import sh
import subprocess
import commands
import MySQLdb
import boto3

con={'host':'q4database.cese7zaylqy5.us-east-2.rds.amazonaws.com', 'username': 'shwetha','password':'password','db':'q4database'}
db = MySQLdb.connect(con['host'],con['username'],con['password'],con['db'])

s3=boto3.resource('s3', aws_access_key_id='AKIAIY2OC2JCTFWADCDQ', aws_secret_access_key='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', region_name='us-east-2')
bucket=s3.Bucket('a3files')
bucket1=s3.Bucket('a3usercredentials')

@app.route('/')
def hello_world():
  return render_template('indexPage.html')

@app.route('/uploaddata',methods=['POST', 'GET'])
def uploaddata():
    cursor = db.cursor()
    startTime = time.time()
    query= "CREATE TABLE classes(Dep Varchar(5), CourseNo  INT, Section INT, CourseTitle Varchar(50), Instructor Varchar(30), Days Varchar(8), \
    StartTime Varchar(30), EndTime	Varchar(30), Max INT, Enrolled	INT)"
    cursor.execute(query)
    db.commit()
    #cursor.execute("create index index1 on uc (city(20),population)")
    #db.commit()
    query = """LOAD DATA LOCAL INFILE '/home/ubuntu/flaskapp/Classes.csv' INTO TABLE classes FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES """
    cursor.execute(query)
    db.commit()
    cursor.execute("SELECT * FROM classes")
    noRows = len(cursor.fetchall())
    endTime = time.time()
    timeTaken = endTime - startTime
    noRows = 140
    return "Shwetha Lathi - 1001192139 - Cloud Computing <br><br>"+str(timeTaken)+" seconds was taken to create table and upload data!\n"+str(noRows)+" rows were created"

@app.route('/lifiles', methods=['POST','GET'])
def lifiles():

  lists=''
  for obj in bucket.objects.all():
    lists=lists+obj.key+"<br>"
    print(obj.key)
  return lists

@app.route('/login', methods=['POST'])
def login():
    global uname
    global dId
    cursor = db.cursor()
    username= request.form['uname']
    password= request.form['psw']
    uname=username
    #value = db.user.find({'username': username, 'password':password}).count()
    query = "select * from login where user=\'"+str(username)+"\' and password=\'"+str(password)+"\'"
    #return query
    cursor.execute(query)
    res = cursor.fetchall()
    length = len(res)
    #return str(length)
    if length < 1:
       	return render_template('home.html', text1="Invalid Username or Password, try again!")
    else:
  	return render_template('indexPage.html')

@app.route('/logout')
def logout():
  return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    global uname
    global dId
    startTime = time.time()
    f= request.files['file']
    file_name=f.filename
    file_content=f.read()
    s3.Bucket('a3files').put_object(Key=file_name, Body=file_content, Metadata={'test':'description test'})
    endTime = time.time()
    timeTaken = endTime - startTime
    return str(timeTaken)+" seconds was taken <br> <br> Shwetha Lathi - 1001192139 - file uploaded"

@app.route('/download', methods=['POST', 'GET'])
def download():
    global uname
    global dId
    file_name = request.args.get('dwnldfile', '')
    for obj in bucket.objects.all():
       if file_name == obj.key:
          file = obj.get()["Body"].read()
          response = make_response(file)
          response.headers["Content-Disposition"] = "attachment; filename=" + file_name
          return response
    return "File Not Found"

@app.route('/view', methods=['POST','GET'])
def lists():
  global uname
  global dId
  startTime = time.time()
  lists=[]
  for obj in bucket.objects.all():
    lists.append(obj.key)
  #return str(lists)
  endTime = time.time()
  timeTaken = endTime - startTime
  return render_template('view.html', lists=lists)

@app.route('/delete', methods=['POST','GET'])
def delete():
    finallist=[]
    for obj in bucket.objects.all():
      finallist.append(obj.key)
    #return str(finallist)
    return render_template('delview.html', lists=finallist)

@app.route('/del/<name>', methods=['POST','GET'])
def delt(name):
  file_name = name
  for obj in bucket.objects.all():
    if file_name == obj.key:
          obj.delete()
          return 'File deleted'

@app.route('/back')
def back():
   return render_template('indexPage.html')

@app.route('/graph',methods=['POST', 'GET'])
def graphd():
    return render_template('scatter.html')

if __name__ == '__main__':
  app.run()
