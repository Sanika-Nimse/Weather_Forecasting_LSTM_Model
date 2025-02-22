import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import requests
from datetime import datetime, timedelta
from tkinter import messagebox 

# Replace with your OpenWeatherMap API key
api_key = 'd0f4215f39312e5de368ee8edad554b8'

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Weather Prediction App')
        self.root.configure(bg='#FFD700')
       
        self.create_widgets(root)

    def create_widgets(self, page):
        self.city_label = ttk.Label(frame_alpr, text='Enter City:')
        self.city_label.grid(row=0, column=0, padx=10, pady=10)

        self.city_entry = ttk.Entry(frame_alpr)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        self.hours_label = ttk.Label(frame_alpr, text='Enter Hours:')
        self.hours_label.grid(row=1, column=0, padx=10, pady=10)

        self.hours_entry = ttk.Entry(frame_alpr)
        self.hours_entry.grid(row=1, column=1, padx=10, pady=10)

        self.predict_button = ttk.Button(frame_alpr, text='Predict Weather', command=lambda: self.predict_weather(page))
        self.predict_button.grid(row=2, column=0, columnspan=2, pady=10)

        
    def predict_weather(self, page):
        city = self.city_entry.get()
        hours = self.hours_entry.get()

        if not city or not hours.isdigit():
            messagebox.showwarning('Weather Prediction', 'Please enter valid city and hours.')
            return

        weather_data = fetch_weather_data(city)

        if weather_data:
            sequence_length = 1  # For per hour predictions
            future_hours = int(hours)

            features, targets = prepare_data(weather_data, sequence_length)

            scaler = MinMaxScaler()
            features_scaled = scaler.fit_transform(features[:, :-1])

            X = []
            for i in range(len(features_scaled) - sequence_length):
                X.append(features_scaled[i:i + sequence_length])

            X = np.array(X)

            num_conditions = targets.shape[1] - 3
            model = build_lstm_model((X.shape[1], X.shape[2]))

            early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
            model.fit(X, targets, epochs=50, validation_split=0.2, callbacks=[early_stopping])

            future_data = features[-sequence_length:]
            predictions = make_predictions(model, future_data, sequence_length, future_hours)

            result_text = f"City: {city}\n\nPredicted Weather for the next {future_hours} hours:\n\n"

            for hour, pred in enumerate(predictions, 1):
                temperature, humidity, rainfall, weather_description = pred
                weather_description = map_weather_condition(weather_description)
            
                result_text += (
                    f"Per {hour}.hr:\n"
                    f"Temperature: {pred[0]:.2f}°C\n"
                    f"Humidity: {pred[1]:.2f}%\n"
                    f"Rainfall: {pred[2]:.2f} mm\n"
                    f"Weather Description: {weather_description}\n"
                    f"________________________________________________\n\n"
                )

#self.result_label.config(text=result_text)
            self.result_text = scrolledtext.ScrolledText(page, wrap=tk.WORD, width=70, height=25)
            self.result_text.grid(row=3, column=5, columnspan=2, pady=220,padx=600)

            self.result_text.delete(1.0, tk.END)  # Clear previous content
            self.result_text.insert(tk.END, result_text)


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
        messagebox.showwarning('Weather Prediction', f"Failed to fetch data for {city}. Check your API key and try again.")

        
        return None


def prepare_data(data, sequence_length):
    features = np.array([
        [entry['main']['temp'], entry['main']['humidity'], entry.get('rain', {}).get('3h', 0),
         entry['weather'][0]['id']]
        for entry in data
    ])

    weather_description_mapping = {
        'Thunderstorm': 1,
        'Drizzle': 2,
        'Rain': 3,
        'Snow': 4,
        'Clear': 5,
        'Cloudy': 6,
        'Unknown': 7
    }

    features[:, 3] = [weather_description_mapping.get(desc, 7) for desc in features[:, 3]]

    targets = features[sequence_length:]

    return features[:len(targets)], targets


def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape))
    model.add(Dense(4, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


def make_predictions(model, data, sequence_length, future_hours):
    model=""
    predictions = []

    for i in range(future_hours):
        input_data = data[-sequence_length:].reshape(1, sequence_length, len(data[0]))
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


if __name__ == "__main__":
    root = tk.Tk()
    w,h = root.winfo_screenwidth(),root.winfo_screenheight()
    root.geometry("%dx%d+0+0"%(w,h))
    
    image2 =Image.open('img.jpg')
    image2 =image2.resize((w,h), Image.ANTIALIAS)
    
    background_image=ImageTk.PhotoImage(image2)
    
    background_label = tk.Label(root, image=background_image)
    
    background_label.image = background_image
    
    background_label.place(x=0, y=0)
    #, relwidth=1, relheight=1)
    
    w = tk.Label(root, text="Weather Forecasting and Predication System",width=75,background="#87CEEB",fg="black", height=2,font=("Times new roman",27,"bold"))
    w.place(x=0,y=0)

    
    frame_alpr = tk.LabelFrame(root, text="", width=250, height=250, font=('times', 14, ' bold '),bg="#87CEEB")
    frame_alpr.grid(row=0, column=0, sticky='nw')
    frame_alpr.place(x=100, y=300)
    
    app = WeatherApp(root)
    root.mainloop()
