from flask import Flask,request, make_response, flash, render_template
import pandas
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates
from sklearn.decomposition import PCA
from csv import reader
from dateutil import parser
import numpy as np
import time

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/input', methods=['POST'])
def inpt():
    num = int(float(request.form['num']))
    games = pandas.read_csv("/home/ubuntu/flaskapp/data1.csv")
    start = time.time()
        #cluster
    with open('/home/ubuntu/flaskapp/data1.csv', 'r') as f:
                data = list(reader(f))
    year = [i[1] for i in data[1::]]
    minage = [i[2] for i in data[1::]]

    kmeans_model = KMeans(n_clusters=num, random_state=1)
    # Get only the numeric columns from games.
    good_columns = games._get_numeric_data().dropna(axis=1)
    # Fit the model using the good columns.
    kmeans_model.fit(good_columns)
    # Get the cluster assignments.
    labels = kmeans_model.labels_
    centroids = kmeans_model.cluster_centers_
    pca_2 = PCA(2)
    # Fit the PCA model on the numeric columns from earlier.
    plot_columns = pca_2.fit_transform(good_columns)
    # Make a scatter plot of each game, shaded according to cluster assignment.
    plt.scatter(x=np.array(year), y=np.array(minage))
    plt.savefig('/home/ubuntu/flaskapp/static/scatter.png')
    plt.close()
    #plt.scatter(x=(year), y=(minage), c=np.array(labels))
    plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", linewidths = 5, zorder = 10)
    plt.savefig('/home/ubuntu/flaskapp/static/scatterdata.png')
    plt.close()
    end = time.time()
    timeTaken = end - start
    nofOfPoints1 = len(kmeans_model.cluster_centers_[0])
    nofOfPoints2 = len(kmeans_model.cluster_centers_[1])
    nofOfPoints3 = len(kmeans_model.cluster_centers_[2])
    nofOfPoints4 = len(kmeans_model.cluster_centers_[3])
    nofOfPoints5 = len(kmeans_model.cluster_centers_[4])
    count1 = str(labels).count('0')
    count2 = str(labels).count('1')
    count3 = str(labels).count('2')
    count4 = str(labels).count('3')
    count5 = str(labels).count('4')

    return "centroid 1: "+str(centroids[:, 0][0])+ " "+ str(centroids[:, 0][1])+"<br><br> time: "+"centroid 2: "+str(centroids[:, 1][0])+ " "+ \
        str(centroids[:, 1][1])+"centroid 3: "+str(centroids[:, 2][0])+ " "+ str(centroids[:, 2][1])+ \
        "centroid 4: "+str(centroids[:, 3][0])+ " "+ str(centroids[:,3][1])+"centroid 5: "+str(centroids[:, 4][0])+ " "+ str(centroids[:, 4][1])+"<br><br> time: "+str(timeTaken)+" seconds"+ \
        "<br><br> cluster1 length: "+str(count1)+"<br><br> cluster2 length: "+str(count2)+"<br><br> cluster3 length: "+str(count3)+ \
        "<br><br> cluster4 length: "+str(count4)+"<br><br> cluster5 length: "+str(count5)+"<br><br>"+str(len(labels))+" Total points"

        #bar graph
    inp=[5, 7, 7, 8, 12]
    ax = inp.plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("yearpublished", fontsize=12)
    ax.set_ylabel("minplaytime", fontsize=12)
    plt.show()
    plt.savefig('/home/ubuntu/flaskapp/static/bardata.png')
    plt.close()
    return render_template('index.html')

@app.route('/select', methods=['POST'])
def select():
    num = int(float(request.form['num1']))
    col1 = str(request.form['col1'])
    col2 = str(request.form['col2'])
    if(col1 == "House"):
                index1 = 0
    if(col1 == "District"):
            index1 = 1
    if(col1 == "Sector"):
           index1 = 2
    if(col1 == "City"):
           index1 = 3
    if(col2 == "House"):
                index2 = 0
    if(col2 == "District"):
            index2 = 1
    if(col2 == "Sector"):
           index2 = 2
    if(col2 == "City"):
           index2 = 3
    col2 = str(request.form['col2'])
    games = pandas.read_csv("/home/ubuntu/flaskapp/data1.csv")
    start = time.time()
        #cluster
    with open('/home/ubuntu/flaskapp/data1.csv', 'r') as f:
                data = list(reader(f))
    year = [i[int(index1)] for i in data[1::]]
    minage = [i[int(index2)] for i in data[1::]]

    kmeans_model = KMeans(n_clusters=num, random_state=1)
    # Get only the numeric columns from games.
    good_columns = games._get_numeric_data().dropna(axis=1)
    # Fit the model using the good columns.
    kmeans_model.fit(good_columns)
    # Get the cluster assignments.
    labels = kmeans_model.labels_
    centroids = kmeans_model.cluster_centers_
    pca_2 = PCA(2)
    # Fit the PCA model on the numeric columns from earlier.
    plot_columns = pca_2.fit_transform(good_columns)
    # Make a scatter plot of each game, shaded according to cluster assignment.
    plt.scatter(x=np.array(year), y=np.array(minage))
    #plt.scatter(x=(year), y=(minage), c=np.array(labels))
    #plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)
    plt.title('MinAge over Year')
    plt.xlabel('Year')
    plt.ylabel('MinAge')
    #plt.savefig('/home/ubuntu/flaskapp/static/scatterdata.png')
    plt.close()
    end = time.time()
    timeTaken = end - start
    count1 = str(labels).count('0')
    count2 = str(labels).count('1')
    count3 = str(labels).count('2')
    count4 = str(labels).count('3')
    count5 = str(labels).count('4')
    return "centroid 1: "+str(centroids[:, 0][0])+ " "+ str(centroids[:, 0][1])+"<br><br> time: "+"centroid 2: "+str(centroids[:, 1][0])+ " "+ \
        str(centroids[:, 1][1])+"centroid 3: "+str(centroids[:, 2][0])+ " "+ str(centroids[:, 2][1])+ \
        "centroid 4: "+str(centroids[:, 3][0])+ " "+ str(centroids[:,3][1])+"centroid 5: "+str(centroids[:, 4][0])+ " "+ str(centroids[:, 4][1])+"<br><br> time: "+str(timeTaken)+" seconds"+ \
        "<br><br> cluster1 length: "+str(count1)+"<br><br> cluster2 length: "+str(count2)+"<br><br> cluster3 length: "+str(count3)+ \
        "<br><br> cluster4 length: "+str(count4)+"<br><br> cluster5 length: "+str(count5)+"<br><br>"+str(len(labels))+" Total points"

        #bar graph
    inp=[5, 7, 7, 8, 12]
    ax = np.array(inpt).plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("yearpublished", fontsize=12)
    ax.set_ylabel("minplaytime", fontsize=12)
    plt.show()
    plt.savefig('/home/ubuntu/flaskapp/static/bardata.png')
    plt.close()
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host="0.0.0.0",debug ='True')
