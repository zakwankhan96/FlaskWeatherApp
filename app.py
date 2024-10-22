#import all the required libraries
import pandas as pd
import csv
import sqlite3
import joblib
from flask import Flask, render_template, request, redirect
import requests


#initialising the application
app = Flask(__name__)


#defining the function to get current weather details from the API
def get_current_weather(city):
    
    #API Key to get weather details
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    
    querystring = {"q":city,"days":"1"}

    header = {"X-RapidAPI-Key": "xxxxxxxxxxxx","X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    response = requests.get(url, headers=header, params=querystring)
    
    #Read data from response
    data = response.json()
    
    # get the required details from the response
    location=data['location']
    current_weather=data['current']
    forecastday=data['forecast']['forecastday'][0]
    astro=data['forecast']['forecastday'][0]['astro']
    hour=data['forecast']['forecastday'][0]['hour'][0]
    city=location['name']
    region=location['region']
    country=location['country']
    time=location['localtime']
    temperature=current_weather['temp_c']
    weather=current_weather['condition']['text']
    weather_ico=current_weather['condition']['icon']
    max_temp=forecastday['day']['maxtemp_c']
    min_temp=forecastday['day']['mintemp_c']
    day_forecast=forecastday['day']['condition']['text']
    day_forecast_ico=forecastday['day']['condition']['icon']
    uv=forecastday['day']['uv']
    dew_point=hour['dewpoint_c']
    windspeedKmph=current_weather['wind_kph']
    winddirDegree=current_weather['wind_degree']
    windDirection=current_weather['wind_dir']
    pressure=current_weather['pressure_mb']
    humidity=current_weather['humidity']
    precipitation=current_weather['precip_mm']
    cloudcover=current_weather['cloud']
    feelslike=current_weather['feelslike_c']
    visibility=current_weather['vis_km']
    wind_gust=current_weather['gust_kph']
    sunrise= astro['sunrise']
    sunset=astro['sunset']

    return (city, region, country, time, temperature, weather, weather_ico, max_temp,
            min_temp, feelslike, pressure, humidity, precipitation, cloudcover, uv,
            dew_point, visibility, windspeedKmph, winddirDegree, windDirection, day_forecast, 
            day_forecast_ico, wind_gust, sunrise, sunset)

#defining the function to get hourly forecast
def get_hour_forecast(city):
    
    # defining the API Key and the url to get the hourly weather details
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    
    querystring = {"q":city,"days":"1"}

    header = {"X-RapidAPI-Key": "xxxxxxxxxxxxxxxxxxx","X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}

    response = requests.get(url, headers=header, params=querystring)
    
    #Read data from response
    data = response.json()
    forecastday=data['forecast']['forecastday']
    
    # create an empty list to store the forecast data
    hourly_data=[]
    
    for day in forecastday:
        hour_data= day['hour'] 
        
        # extract the data for each hour from the response
        for i in range(0, len(hour_data)):
            hour= hour_data[i]['time'].split()[1]
            temp_c= hour_data[i]['temp_c']
            icon=hour_data[i]['condition']['icon']
            
            # append the extracted data into the list
            hourly_data.append({'hour':hour,'temp_c':temp_c,'icon':icon})
    
    return hourly_data


#Function to get three day forecast
def get_threeday_forecast(city):
    
    # defining the API Key and the url to get three day weather details
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    
    querystring = {"q":city,"days":"3"}
    
    header = {"X-RapidAPI-Key": "xxxxxxxxxxxxxxxxxx","X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    
    response = requests.get(url, headers=header, params=querystring)
    
    #Reading the data from the response
    data = response.json()
    forecastday=data['forecast']['forecastday']
    
    # create an  empty list to store the forecast data
    threeday_data=[]

    for forecast in forecastday:
        
        # extract the three day forecast data from the response
        date=forecast['date']
        maxtemp_c=forecast['day']['maxtemp_c']
        mintemp_c=forecast['day']['mintemp_c']
        cond_text=forecast['day']['condition']['text']
        cond_icon=forecast['day']['condition']['icon']
        
        # append the extracted the data into the list
        threeday_data.append({'date':date, 'maxtemp_c':maxtemp_c, 'mintemp_c':mintemp_c, 'cond_text':cond_text, 'cond_icon':cond_icon})
    
    return threeday_data

#Defining the app route to load the homepage while launching the app
@app.route('/')
def home():
    
    # specify the default city when the app launches
    city='Aligarh'
    
    # get the weather details from the API using the defined functions
    current_weather= get_current_weather(city)
    hourly_forecast=get_hour_forecast(city)
    threeday_forecast=get_threeday_forecast(city)
    
    # reder the home page when the app launches with the weather details of the default city
    return render_template('index.html', curr_weather=current_weather, 
                            hourly_forecast=hourly_forecast, 
                            threeday_forecast=threeday_forecast, city=city, cities=get_city())


#defining the app route for showing the weather forecast for the user specified city
@app.route('/forecast', methods=['POST'])
def forecast():
    
    # get the city name from the user via form submission in the app
    city=request.form.get('city')
    if not city:
        city = request.args.get('city')
    
    # get weather details from the API using the defined functions 
    current_weather= get_current_weather(city)
    hourly_forecast=get_hour_forecast(city)
    threeday_forecast=get_threeday_forecast(city)
    
    # render the home page with the details of the user specified city
    return render_template('index.html', curr_weather=current_weather, 
                            hourly_forecast=hourly_forecast,
                            threeday_forecast=threeday_forecast, city=city)


# defining the details route to show the weather details for the city
@app.route('/details')
def details():
    
    # get city name from the app via form submission
    city=request.args.get('city')

    # get weather details for the city from the API using the defined functions
    curr_weather=get_current_weather(city)
    hourly_forecast=get_hour_forecast(city)
    threeday_forecast=get_threeday_forecast(city)

    # render the details page to show the weather details for the user specified city
    return render_template('details.html', curr_weather=curr_weather,
                            hourly_forecast=hourly_forecast, 
                            threeday_forecast=threeday_forecast, city=city)


# defining the route to show the list cities from the database and weather conditions
@app.route('/cities')
def get_city():
    
    # create a connection to the database
    conn=sqlite3.connect('city_db.db')
    cursor=conn.cursor()

    # execute the SQL query to fetch the cities from the database
    cursor.execute("Select City from City")
    cities=cursor.fetchall()

    # create an empty list to hold the cities weather information
    city_weather_details=[]
    for city in cities:
        city_name=city[0]
        # get weather details for the list of cities using the API
        weather_details=get_current_weather(city_name)
        city_weather_details.append(weather_details)
    # terminate the connection to the databse   
    cursor.close()
    conn.close()
    # render the cities page to show the weather information about the cities in the list
    return render_template('cities.html', city_curr_weather=city_weather_details,cities=cities,)


# defining the route to show the weather details for a city from the cities list
@app.route('/showDetails', methods=['POST'])
def showDetails():
    
    # get city name from the app via form
    city= request.form.get('city')
    # get weather details for the selected city from the API
    curr_weather=get_current_weather(city)
    hourly_forecast=get_hour_forecast(city)
    threeday_forecast=get_threeday_forecast(city)
    # render the details page to show the weather details for the selected city
    return render_template('details.html', city=city, 
                            curr_weather=curr_weather, 
                            hourly_forecast=hourly_forecast, 
                            threeday_forecast=threeday_forecast)


# defining the route for adding a city into the cities list
@app.route('/add_city', methods=['POST'])
def add_city():
    
    # get city name from the app via form submission
    city_name=request.form.get('city_name')

    # create a connection to the city database
    conn= sqlite3.connect('city_db.db')
    cursor=conn.cursor()
    
    # execute the SQL command to add the city into the database
    cursor.execute('insert into City ("City") values (?)', (city_name,))
    
    # commit the changes to the database
    conn.commit()
    
    # terminate the connection
    cursor.close()
    conn.close()
    
    # redirect to the cities route for rendering the new updated list
    return redirect('/cities')


# defining the route for removing a city from the cities list
@app.route('/remove_city', methods=['POST'])
def remove_city():
    
    # get the city from the app via form submission
    city_name=request.form['city_name']
    
    # create a connection to the city databse
    conn= sqlite3.connect('city_db.db')
    cursor=conn.cursor()
    
    # execute SQL command to remove the city from the database
    cursor.execute('delete from City where City= ?', (city_name,))
    
    # commit the changes to the database
    conn.commit()
    
    # terminate the connection
    cursor.close()
    conn.close()
    
    # redirect to the cities route for rendering the new updated list
    return redirect('/cities')


# Load the prediction models for each city
xgb_ben = joblib.load('xgboost_benga.pkl')
xgb_bom = joblib.load('xgboost_bom.pkl')
xgb_del = joblib.load('xgboost_del.pkl')
xgb_hyd = joblib.load('xgboost_hyd.pkl')
xgb_jai = joblib.load('xgboost_jai.pkl')
xgb_kan = joblib.load('xgboost_kan.pkl')
xgb_nag = joblib.load('xgboost_nag.pkl')
xgb_pune = joblib.load('xgboost_pune.pkl')


#Define the route for prediction using the trained XGBoost Models
@app.route('/predict', methods=['POST'])
def predict():
    
    #Get City from form
    city = request.form['city']
    city = city.lower()
    
    if city == 'bengaluru':
        model_xgb = xgb_ben

    elif city == 'bombay':
        model_xgb = xgb_bom

    elif city == 'new delhi':
        model_xgb = xgb_del

    elif city == 'hyderabad':
        model_xgb = xgb_hyd

    elif city == 'jaipur':
        model_xgb = xgb_jai

    elif city == 'kanpur':
        model_xgb = xgb_kan

    elif city == 'nagpur':
        model_xgb = xgb_nag

    elif city == 'pune':
        model_xgb = xgb_pune
    else:
        return redirect('/')

    #Get Weather Details using the API
    current_weather= get_current_weather(city)
    hourly_forecast= get_hour_forecast(city)
    threeday_forecast=get_threeday_forecast(city)
    
    # select the features to use for predicting the weather
    features= ['maxtempC', 'mintempC','DewPointC','FeelsLikeC',
                'cloudcover','humidity','precipMM', 'pressure', 
                'visibility', 'winddirDegree', 'windspeedKmph']
    
    data={'maxtempC':current_weather[7],'mintempC':current_weather[8],'DewPointC':current_weather[15], 
            'FeelsLikeC':current_weather[9], 'cloudcover':current_weather[13], 'humidity':current_weather[11], 
            'precipMM':current_weather[12], 'pressure':current_weather[10], 'visibility':current_weather[16], 
            'winddirDegree':current_weather[17], 'windspeedKmph':current_weather[18]}

    # writing the features values to a csv file
    with open('conditions.csv', 'w') as file:
        writeToFile=csv.DictWriter(file, fieldnames=features)
        writeToFile.writeheader()
        writeToFile.writerow(data)

    # loading the csv file
    df= pd.read_csv('conditions.csv')
    
    # preparing data for prediction using the XGBoost Model
    
    user_input = df.astype(float)
    user_input = user_input.drop_duplicates()
    user_input = user_input.reset_index(drop=True)

    #Predicting the temperature the using the feature values from the csv file
    prediction_xgb = model_xgb.predict(user_input) 
    
    # preparing the predicted temperature value for use in the application
    prediction_xgb= prediction_xgb[0]
    predicted_temp= round(prediction_xgb, 2)

    # rendering the prediction page to show the predicted temperature along with the rest of the details
    return render_template('prediction.html', curr_weather= current_weather,
                            hourly_weather= hourly_forecast,
                            threeday_weather= threeday_forecast,
                            predicted_temp= predicted_temp)

if __name__ == '__main__':
    app.run(debug=True)
