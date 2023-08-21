#import the required libraries
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pickle

# Step 1: Load the dataset
df = pd.read_csv("hyderabad.csv")

# Step 2: Preprocessing the data
df['date_time'] = pd.to_datetime(df['date_time'])
df.set_index('date_time', inplace=True)
print(df.index)
# Step 3: Feature selection
features = ['maxtempC', 'mintempC','DewPointC','FeelsLikeC', 
            'cloudcover','humidity','precipMM', 'pressure', 
            'visibility', 'winddirDegree', 'windspeedKmph']
# Step 4: Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df['tempC'], test_size=0.5, random_state=42)

# Step 5: Training the XGBoost model
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# Step 6: Evaluating the model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)



# Save the model to a file
model_filename = "xgboost_hyd.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(model, file)
    print("model saved")


model_filename = "xgboost_hyd.pkl"
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Prepare the input data for prediction
input_data = pd.DataFrame({
    'maxtempC': [31.9],  # Example input values, modify as needed
    'mintempC': [24.7],
    'DewPointC': [23.2],
    'FeelsLikeC': [37.6],
    'cloudcover': [25],
    'humidity': [71],
    'precipMM': [0],
    'pressure': [1006],
    'visibility': [5],
    'winddirDegree': [290],
    'windspeedKmph': [19.1]
})

# Predict the temperature
predicted_temp = model.predict(input_data)

# Print the predicted temperature
print("Predicted Temperature (tempC):", predicted_temp)
