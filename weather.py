

# Replace with your OpenWeatherMap API key
import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

# Replace with your OpenWeatherMap API key
api_key = 'd0f4215f39312e5de368ee8edad554b8'

# Function to fetch weather data for a given city
def fetch_weather_data(city):
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        return data['list']
    else:
        print(f"Failed to fetch data for {city}. Check your API key and try again.")
        return None
    
# Function to process and prepare data for LSTM
def prepare_data(data, sequence_length):
    features = np.array([
        [entry['main']['temp'], entry['main']['humidity'], entry.get('rain', {}).get('3h', 0), entry['weather'][0]['id']]
        for entry in data
    ])

    # Convert weather description to a numerical format (you can use a mapping function)
    weather_description_mapping = {
        'Thunderstorm': 1,
        'Drizzle': 2,
        'Rain': 3,
        'Snow': 4,
        'Clear': 5,
        'Cloudy': 6,
        'Unknown': 7
    }

    # Map weather descriptions to numerical values
    features[:, 3] = [weather_description_mapping.get(desc, 7) for desc in features[:, 3]]

    # Create target sequences shifted by one time step
    targets = features[sequence_length:]

    return features[:len(targets)], targets

# Function to build and train the LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape))
    model.add(Dense(4, activation='linear'))  # Adjust as needed, 4 for temperature, humidity, rainfall, and weather condition
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model

def make_predictions(model, data, sequence_length, future_days):
    predictions = []

    for i in range(future_days):
        input_data = data[-sequence_length:].reshape(1, sequence_length, len(data[0]))
        # Modify the input_data to include only the relevant features (e.g., first 3 features)
        input_data = input_data[:, :, :3]
        prediction = model.predict(input_data)
        predictions.append(prediction[0])
        data = np.vstack([data, np.array([prediction[0]])])

    return predictions
def map_weather_condition(condition_id):
    if 0 <= condition_id < 1:  # Thunderstorm
        return "Thunderstorm"
    elif 2 <= condition_id < 3:  # Drizzle
        return "Drizzle"
    elif 3 <= condition_id < 4:  # Rain
        return "Rain"
    elif 4 <= condition_id < 5:  # Snow
        return "Snow"
    elif condition_id == 5:  # Clear sky
        return "Clear"
    elif 5 <= condition_id <= 6:  # Cloudy
        return "Cloudy"
    else:
        return "Unknown"
def main():
    cities = ['Pune', 'Nashik', 'Mumbai']  # Add your list of cities
    # For per day predictions
    sequence_length = 8  # Adjust as needed (e.g., if data is collected every 3 hours, and you want to predict for 24 hours, set to 8)
    future_days = 5  # Adjust as needed (number of days to predict)
    for city in cities:
        weather_data = fetch_weather_data(city)

        if weather_data:
            features, targets = prepare_data(weather_data, sequence_length)

            # Normalize features
            scaler = MinMaxScaler()
            features_scaled = scaler.fit_transform(features[:, :-1])  # Exclude the last column (weather description) for normalization

            X = []
            for i in range(len(features_scaled) - sequence_length):
                X.append(features_scaled[i:i+sequence_length])

            X = np.array(X)

            num_conditions = targets.shape[1] - 3  # Exclude continuous variables from the count
            model = build_lstm_model((X.shape[1], X.shape[2]))

            early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
            model.fit(X, targets, epochs=50, validation_split=0.2, callbacks=[early_stopping])

            future_data = features[-sequence_length:]
            predictions = make_predictions(model, future_data, sequence_length, future_days)

            print(f"City: {city}")
            print(f"Predicted Weather for the next {future_days} days:")
            for day, pred in enumerate(predictions, 1):
                temperature, humidity, rainfall, weather_description = pred
                weather_description = map_weather_condition(weather_description)
                print(f"Day {day}: Temperature: {pred[0]:.2f}°C, Humidity: {pred[1]:.2f}%, Rainfall: {pred[2]:.2f} mm, Weather Description: {weather_description}")
            print("="*50)

if __name__ == "__main__":
    main()