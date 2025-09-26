# -*- coding: utf-8 -*-
#import libraries
# import mysql.connector
import numpy as np
import requests , json
from flask import Flask, render_template,request
import http.client
import pickle#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('model_edited.pkl', 'rb'))
# model_r = pickle.load(open('model.pkl', 'rb'))        #model for the manual crop prediction including rainfall

#default page of our web-app

@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/form')
def form():
    return render_template('./form.html')

#To use the predict button in our web-app

@app.route('/predict',methods=['POST'])
def predict():
    #For rendering results on HTML GUI
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    # print(final_features)
    prediction = model.predict(final_features)
    output = prediction 
    return render_template('./result.html', prediction_text=f'{output[0].capitalize()}')

# IoT Based crop prediction 
# [displays values corresponding to various parameter and predicts the crop using ML model]

# @app.route('/Iot')
# def IoT_ML():
    
#     # print(final_features)
#     # prediction = model.predict(final_features)
#     # output = prediction 

#     mydb = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="soil_parameter"

#             )
#     mycursor = mydb.cursor()

#     mycursor.execute("SELECT * FROM params")  # executing the query to retrive the data

#     # Returns list of tuples (records in soil_parameter database)
#     myres = mycursor.fetchall()

#     # reverses the tuples in the list fist to last / last to first 
#     # to fetch recently added data into the database
#     # recently added record to db is stored at the bottom of the db table so we are reversing 

#     myres.reverse()        

#     # print(type(myres))
#     # print(type(list(myres[0])))
#     tup = myres[0]
#     int_features = list(myres[0])
#     final_features = [np.array(int_features)]
#     # print(final_features)

#     # Giving input to the model trained machine learning model

#     prediction = model.predict(final_features)


#     return render_template('./IoT_ML.html',prediction_text=f'{prediction[0].capitalize()}',N=tup[0],P=tup[1],K=tup[2],Temp=tup[3],Humid=tup[4],pH=tup[5])

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# Retriving the data from the cloud and giving to the model as intput

@app.route('/Iot')
def IoT_ML():
    import requests
    data=requests.get("https://api.thingspeak.com/channels/2900389/feeds.json?api_key=0QLB3KNKJI62Q9E8&results=2")
    n     = float(data.json()['feeds'][-1]['field4'])
    p     = float(data.json()['feeds'][-1]['field5'])
    k     = float(data.json()['feeds'][-1]['field6'])
    temp  = float(data.json()['feeds'][-1]['field2'])
    hum   = float(data.json()['feeds'][-1]['field3'])
    ph    = float(data.json()['feeds'][-1]['field7'])

    prediction = model.predict([[n,p,k,temp,hum,ph]])[0]


    return render_template('./IoT_ML.html',prediction_text=f'{prediction.capitalize()}',N=n,P=p,K=k,Temp=temp,Humid=hum,pH=ph)


@app.route('/weather', methods= ['POST', 'GET'])
def weather():
    # print(request.method)
    if request.method == "POST":
        location = request.form.get("place")
        # print(location)
        api_key ='03b1acbfd0387ac994dad57eb102fe01'
        
        link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api_key
        api_link = requests.get(link)
        data = api_link.json()
        # print(data)
        temp= round((data['main']['temp'])-273.15,2)
        humidity=data['main']['humidity']
        pressure1=data['main']['pressure']
        # weather_desc = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']
        place =data['name']
        visible=data['visibility']
        latitude=data['coord']['lat']
        longitude=data['coord']['lon']
        # return render_template('./weather.html', info=data,tempr=temp,desc=weather_desc,speed=wind_speed,humid=humidity,pressure=pressure1,placeo=place)
    else:
        api_key ='03b1acbfd0387ac994dad57eb102fe01'
        location = 'Kolar'
        link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api_key
        api_link = requests.get(link)
        data = api_link.json()
            # print(data)
        temp= round((data['main']['temp'])-273.15,2)
        humidity=data['main']['humidity']
        pressure1=data['main']['pressure']
        # weather_desc = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']
        place =data['name']
        visible=data['visibility']
        latitude=data['coord']['lat']
        longitude=data['coord']['lon']
    return render_template('./weather.html', info=data,tempr=temp,speed=wind_speed,humid=humidity,pressure=pressure1,placeo=place,visible=visible,latitude=latitude,longitude=longitude)

if __name__ == "__main__":
    app.run(debug=True)

