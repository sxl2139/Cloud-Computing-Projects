from flask import Flask,render_template,request,make_response
from azure.storage.blob import BlockBlobService,PublicAccess,ContentSettings,BlobPermissions
import os
import time
import MySQLdb
import string
app = Flask(__name__)

block_blob_service = BlockBlobService(account_name='q7resourcediag254', account_key='NT1aif56hCQelnAsbWQIv1t42FfbZEBmJd+dbg3s0hpPijQsoYDvn+9icHvc2SE1i1YtojSJJDTexkP1CwU9iA==')
con={'host':'us-cdbr-azure-southcentral-f.cloudapp.net', 'username': 'be5e2c65ccc060','password':'8a8375da','db':'q8db'}
db = MySQLdb.connect(con['host'],con['username'],con['password'],con['db'])

uname=''

@app.route('/')
def hello_world():
  return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global uname
    cursor = db.cursor()
    username= request.form['uname']
    password= request.form['pwd']
    uname = username
    query = "select * from login where user=\'"+str(username)+"\' and password=SHA(\'"+str(password)+"\')"
    #return query
    cursor.execute(query)
    res = cursor.fetchall()
    length = len(res)
    #return str(length)
    if length < 1:
       	return render_template('login.html', txt1="Invalid Username or Password, try again!")
    else:
        if(username=='admin'):
  	        return render_template('adminView.html')
        else:
            return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
  cursor = db.cursor()
  startTime = time.time()
  query= "CREATE TABLE food(foodtype Varchar(30), foodname Varchar(30), ingredient Varchar(30), quantity INT)"
  #cursor.execute(query)
  db.commit()
  #cursor.execute("create index index1 on food (foodname(10),ingredient)")
  db.commit()
  query = """LOAD DATA LOCAL INFILE '/home/ubuntu/flaskapp/food.csv' INTO TABLE food FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES """
  #cursor.execute(query)
  db.commit()
  cursor.execute("SELECT * FROM food")
  noRows = len(cursor.fetchall())
  endTime = time.time()
  timeTaken = endTime - startTime
  return "Shwetha Lathi -- 1001192139 - Cloud Computing - Quiz8 <br>"+str(timeTaken)+" seconds was taken to create table and upload data <br>\n"+str(noRows)+" rows were created"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global uname
    startTime = time.time()
    #block_blob_service.create_container('mycontainer', public_access=PublicAccess.Container)
    files= request.files.getlist('file[]')
    #return str(len(files))
    #size = request.form['size']
    for f in files:
        file_name=f.filename
        file_content=f.read()
        file_length = len(file_content)
        block_blob_service.create_blob_from_bytes(
        'mycontainer',
        file_name,
        file_content)
    endTime = time.time()
    timeTaken = endTime - startTime
    return "Shwetha Lathi - 1001192139 - Cloud Computing <br> Uploaded successfully! <br>"+str(timeTaken)+" seconds was taken."

@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    global uname
    startTime = time.time()
    #block_blob_service.create_container('mycontainer', public_access=PublicAccess.Container)
    files= request.files['file']
    return "Added"
    ing = string.split(str(request.form['inping']).split(','))
    quan = string.split(str(request.form['inpquan']).split(','))
    fdname = str(request.form['fdname'])
    fdtype = str(request.form['fdtype'])
    cursor = db.cursor()
    leng = len(ing)
    while(leng > 0):
        query = "insert into food values(\'"+fdtype+"\',\'"+fdname+"\',"+ing[leng]+quan[leng]+")"
        leng -= leng
        cursor.execute(query)
        return leng
    db.commit()
    #return query
    #return str(len(files))
    #size = request.form['size']
    file_name=f.filename
    file_content=f.read()
    file_length = len(file_content)
    block_blob_service.create_blob_from_bytes(
    'mycontainer',
    file_name,
    file_content)
    endTime = time.time()
    timeTaken = endTime - startTime
    return "Shwetha Lathi - 1001192139 - Cloud Computing <br> Inserted successfully! <br>"+str(timeTaken)+" seconds was taken."

@app.route('/view', methods=['POST','GET'])
def lists():
  global uname
  startTime = time.time()
  lists=[]
  container = 'mycontainer'
  for obj in block_blob_service.list_blobs('mycontainer'):
    lists.append(obj.name)
  #return str(lists)
  endTime = time.time()
  timeTaken = endTime - startTime
  return render_template('view.html', lists=lists, container=container, timeTaken=timeTaken)

@app.route('/view/<name>', methods=['POST','GET'])
def delt(name):
  global uname
  startTime = time.time()
  file_name = name
  cursor = db.cursor()
  foodname = file_name.replace('.png','')
  foodname = file_name.replace('.jpg','')
  cursor.execute("create index index4 on food (foodname(10))")
  query = "select count from requests where foodname=\'"+foodname+"\'"
  cursor.execute(query)
  result = cursor.fetchall()
  newcount = 0
  for row in result:
	newcount = int(row[0])+1
  query = "update requests set count="+str(newcount)+" where foodname=\'"+foodname+"\'"
  cursor.execute(query)
  db.commit()
  query = "select ingredient from food where foodname =\'"+foodname+"\'"
  #eturn query
  cursor.execute(query)
  result = cursor.fetchall()
  list = ''
  for row in result:
	list = list+row[0]+","
  #return str(list)
  lists=[]
  ingredients = str(list)
  container = 'mycontainer'
  #return file_name
  for obj in block_blob_service.list_blobs('mycontainer'):
    if(obj.name==file_name):
    	lists.append(obj.name)
  #return str(lists)
  endTime = time.time()
  timeTaken = endTime - startTime
  return render_template('viewIngredients.html', lists=lists, container=container, timeTaken=timeTaken, ingredients=ingredients)

@app.route('/top', methods=['GET', 'POST'])
def top():
    global uname
    startTime = time.time()
    cursor = db.cursor()
    query = "select ingredient,count(ingredient) as count from food group by ingredient order by count(ingredient) desc limit 5"
    cursor.execute(query)
    result = cursor.fetchall()
    list = ''
    for row in result:
  	     list = list+row[0]+","
    endTime = time.time()
    timeTaken = endTime - startTime
    res = "Shwetha Lathi - 1001192139 - Cloud Computing <br> Downloaded successfully!! <br>"+str(timeTaken)+" seconds was taken.<br>"
    return res+str(list)

@app.route('/popular', methods=['GET', 'POST'])
def popular():
    global uname
    startTime = time.time()
    cursor = db.cursor()
    query = "select foodname from requests order by count desc limit 1"
    cursor.execute(query)
    result = cursor.fetchall()
    list = ''
    lists = []
    container = 'mycontainer'
    for row in result:
  	 list = list+row[0]+","
         for obj in block_blob_service.list_blobs('mycontainer'):
           chkname = str(obj.name)
           chkname = chkname.replace('.png','')
           chkname = chkname.replace('.jpg','')
           if(chkname==str(row[0])):
             lists.append(obj.name)
    endTime = time.time()
    timeTaken = endTime - startTime
    res = "Shwetha Lathi - 1001192139 - Cloud Computing <br> Downloaded successfully!! <br>"+str(timeTaken)+" seconds was taken.<br>"
    return render_template('view.html', lists=lists, container=container, timeTaken=timeTaken)

@app.route('/search', methods=['GET', 'POST'])
def search():
    global uname
    startTime = time.time()
    container = 'mycontainer'
    fdType = str(request.form['fdType'])
    #fdName = str(request.form['fdName'])
    calories = str(request.form['calories'])
    #ingredient = str(request.form['ing'])
    #w2 = str(request.form['w2'])
    query = "select foodname from(select foodname,sum(quantity) as total from food where foodtype = \'"+fdType+"\' group by foodname) as tab where tab.total < "+calories
    #return query
    cursor = db.cursor()
    #query = "select DISTINCT foodname from food where ingredient=\'"+ingredient+"\'"
    cursor.execute(query)
    result = cursor.fetchall()
    list = ''
    lists=[]
    for row in result:
  	     list = list+row[0]+","
             for obj in block_blob_service.list_blobs('mycontainer'):
               chkname = str(obj.name)
               chkname = chkname.replace('.png','')
               chkname = chkname.replace('.jpg','')
               if(chkname==str(row[0])):
            	 lists.append(obj.name)
    endTime = time.time()
    timeTaken = endTime - startTime
    res = "Shwetha Lathi - 1001192139 - Cloud Computing <br> Downloaded successfully!! <br>"+str(timeTaken)+" seconds was taken.<br>"
    return render_template('viewIngredients.html', lists=lists, container=container, timeTaken=timeTaken)

@app.route('/download', methods=['GET', 'POST'])
def download():
    global uname
    startTime = time.time()
    file_name = request.args.get('dwnldfile', '')
    b = block_blob_service.get_blob_to_bytes('mycontainer', file_name)
    response = make_response(b.content)
    response.headers["Content-Disposition"] = "attachment; filename=" + file_name
    endTime = time.time()
    timeTaken = endTime - startTime
    res = "Shwetha Lathi - 1001192139 - Cloud Computing <br> Downloaded successfully!! <br>"+str(timeTaken)+" seconds was taken."
    return response

@app.route('/list', methods=['GET', 'POST'])
def list():
    global uname
    startTime = time.time()
    generator = block_blob_service.list_blobs('mycontainer')
    list1 =''
    for blob in generator:
        list1 = list1+blob.name+"<br> "
    endTime = time.time()
    timeTaken = endTime - startTime
    return "Shwetha Lathi - 1001192139 - Cloud Computing <br> "+str(timeTaken)+" seconds was taken.<br>"+str(list1)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    global uname
    startTime = time.time()
    file_name = request.args.get('delfile', '')
    block_blob_service.delete_blob('mycontainer', file_name)
    endTime = time.time()
    timeTaken = endTime - startTime
    return "Shwetha Lathi - 1001192139 - Cloud Computing <br> Deleted successfully! <br>"+str(timeTaken)+" seconds was taken.<br>"

@app.route('/back')
def back():
   return render_template('home.html')

@app.route('/logout')
def logout():
  return render_template('login.html')

if __name__ == '__main__':
  app.run()
