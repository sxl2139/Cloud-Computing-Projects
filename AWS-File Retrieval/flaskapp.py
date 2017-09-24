
#import modules
from flask import Flask,request,make_response
import boto3
import string
app = Flask(__name__)

#Access buckets
s3=boto3.resource('s3', aws_access_key_id='AKIAIY2OC2JCTFWADCDQ', aws_secret_access_key='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', region_name='us-east-2')
filebucket=s3.Bucket('a3files')
loginbucket=s3.Bucket('a3usercredentials')

#validate login
@app.route('/login', methods=['POST'])
def login():
  username= request.form['uname']
  password= request.form['pwd']
  for obj in loginbucket.objects.all():
    file = obj.get()["Body"].read()
    temp=string.split(file,',')
    print temp
    for vals in temp:
      v=str(vals)
      value=string.split(v,' ')
      print value
      if(username==value[0] and password==value[1]):
        return app.send_static_file('index.html')
    return "Login Failed!"

#upload file to storage
@app.route('/upload', methods=['POST'])
def upload():
  f= request.files['file']
  size = request.form['size']
  file_name=f.filename
  file_content=f.read()
  size = 20
  file_length = len(file_content)
  print (file_length)
  #check if the file exists
  for obj in filebucket.objects.all():
        if file_name == obj.key:
                return "File exists"
  #validate the file size 
  if(file_length > size):
        return "File size exceeded given limit"
  s3.Bucket('a3files').put_object(Key=file_name, Body=file_content)
  return "File uploaded"

#download file from storage  
@app.route('/download', methods=['POST', 'GET'])
def download():
  file_name = request.args.get('dwnldfile', '')
  for obj in filebucket.objects.all():
    if file_name == obj.key:
      file = obj.get()["Body"].read()
      response = make_response(file)
      response.headers["Content-Disposition"] = "attachment; filename=" + file_name
      return response
  return "File Not Found"

#delete file from storage
@app.route('/delete', methods=['POST','GET'])
def delete():
  file_name = request.args.get('delfile', '')
  for obj in filebucket.objects.all():
    if file_name == obj.key:
          obj.delete()
          return 'File deleted'
  return "File not Found"

#list files in bucket
@app.route('/filelist', methods=['POST','GET'])
def filelist():

  lists=''
  for obj in filebucket.objects.all():
    lists=lists+obj.key+obj.key.last_modified+"<br>"
    print(obj.key)
  return lists

#navigate to home page
@app.route('/')
def index():
  return app.send_static_file('home.html')

#navigate to home page on logout
@app.route('/logout')
def logout():
  return app.send_static_file('home.html')

if __name__ == '__main__':
  app.run()

