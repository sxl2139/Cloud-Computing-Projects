import os
from flask import Flask,request,render_template
app = Flask(__name__)
import time
from subprocess import call
import sh
import subprocess
import commands

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/findno',methods=['POST', 'GET'])
def command():
    os.system("cd /home/ubuntu/")
    #outs = commands.getoutput('chmod +x run.sh')

    mapv=str(request.form['map'])
    red=str(request.form['red'])

    if(len(mapv)!=0 and len(red)!=0):
        exCmd="hdfs jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -D mapred.map.tasks="+str(mapv)+" -D mapred.reduce.tasks=" +str(red)+" -file /home/ubuntu/mapper.py \
        -mapper /home/ubuntu/mapper.py -file /home/ubuntu/reducer.py -reducer /home/ubuntu/reducer.py -input /input7/data* -output /outQ66"
        copyFile="hdfs dfs -cat /outQ66/part-00000 > /home/ubuntu/flaskapp/templates/outquiz66.txt"
    else:
        exCmd="hdfs jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -file /home/ubuntu/mapper.py \
        -mapper /home/ubuntu/mapper.py -file /home/ubuntu/reducer.py -reducer /home/ubuntu/reducer.py -input /input7/data* -output /outQ66"
        copyFile="hdfs dfs -cat /outQ66/part-00000 > /home/ubuntu/flaskapp/templates/outquiz66.txt"
    startTime = time.time()
    os.system(exCmd)
    os.system(copyFile)
    endTime = time.time()
    timeTaken = endTime - startTime

    filename = "/home/ubuntu/flaskapp/templates/outQuiz65.txt"

    with open(filename, 'r') as f:
        line=f.readlines()
        lines=""
        for x in line:
            lines+="<li>"
            lines += ''.join('{}'.format(x))
            lines += "</li>"
    	    output="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>finish</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            </head>
            <body>
            <form action="cli.py" method="post">
            <h1> Output:</h1>
            <ul>
            %s
            </ul>
            </form>

            </body>
            </html>"""%(lines)
    return exCmd+"<br><br>Shwetha Lathi 1001192139"+str(timeTaken)+" seconds was taken to execute.<br><br>"+output

@app.route('/findinp',methods=['POST', 'GET'])
def commandinp():
    os.system("cd /home/ubuntu/")

    mapv=str(request.form['map1'])
    red=str(request.form['red1'])
    arg1=str(request.form['arg1'])
    arg2=str(request.form['arg2'])
    #arg3=str(request.form['arg3'])

    if(len(mapv)!=0 and len(red)!=0 and len(arg1)!=0 and len(arg2)!=0):
        exCmd="hdfs jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -D mapred.map.tasks="+str(mapv)+" -D mapred.reduce.tasks=" +str(red)+" -file /home/ubuntu/mapper.py \
        -mapper /home/ubuntu/mapper.py "+arg1+" "+arg2+" -file /home/ubuntu/reducer.py -reducer /home/ubuntu/reducer.py -input /input7/data* -output /outQ66"
        copyFile="hdfs dfs -cat /outQ66/part-00000 > /home/ubuntu/flaskapp/templates/outquiz66.txt"

    startTime = time.time()
    os.system(exCmd)
    os.system(copyFile)
    endTime = time.time()
    timeTaken = endTime - startTime

    filename = "/home/ubuntu/flaskapp/templates/out68.txt"

    with open(filename, 'r') as f:
        line=f.readlines()
        lines=""
        for x in line:
            lines+="<li>"
            lines += ''.join('{}'.format(x))
            lines += "</li>"
            output="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>finish</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            </head>
            <body>
            <form action="cli.py" method="post">
            <h1> Output:</h1>
            <ul>
            %s
            </ul>
            </form>

            </body>
            </html>"""%(lines)
    return exCmd+"<br><br>Shwetha Lathi 1001192139"+str(timeTaken)+" seconds was taken to execute.<br><br> Agecount:5"

@app.route('/graph',methods=['POST', 'GET'])
def graphd():
    return render_template('scatter.html')

if __name__ == '__main__':
  app.run()
