import tkinter as tk
from PIL import Image, ImageTk
import requests
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
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
def fetch_hourly_forecast(city):
    api_key = "d0f4215f39312e5de368ee8edad554b8"  # Replace with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data['list']
        forecast_text = ""
        for forecast in forecast_list:
            forecast_time = forecast['dt_txt']
            temperature = forecast['main']['temp']
            weather_description = forecast['weather'][0]['description'].capitalize()
            forecast_text += f"At {forecast_time}: Temperature: {temperature}°C, Weather: {weather_description}\n"

        # Update the text widget
        weather_text.config(state=tk.NORMAL)
        weather_text.delete(1.0, tk.END)
        weather_text.insert(tk.END, forecast_text)
        weather_text.config(state=tk.DISABLED)
    else:
        weather_text.config(state=tk.NORMAL)
        weather_text.delete(1.0, tk.END)
        weather_text.insert(tk.END, "Error fetching data")
        weather_text.config(state=tk.DISABLED)
        
def build_lstm_model(input_shape):
    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Save the model
    model.save("lstm_model.h5")

    # Load the model for predictions
    loaded_model = load_model("lstm_model.h5")

    return loaded_model

# Example usage
input_shape = (10, 1)  # Assuming input sequences of length 10 and 1 feature
loaded_lstm_model = build_lstm_model(input_shape)

# Create Tkinter window
root = tk.Tk()
root.title("Hourly Weather Forecast")
w,h = root.winfo_screenwidth(),root.winfo_screenheight()
root.geometry("%dx%d+0+0"%(w,h))
# Load background image
background_image = Image.open("img.jpg")  # Replace with the path to your image
background_photo = ImageTk.PhotoImage(background_image)

# Create Tkinter widgets with background image
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

w = tk.Label(root, text="Weather Forecasting and Predication System",width=80,background="#87CEEB",fg="black", height=2,font=("Times new roman",27,"bold"))
w.place(x=0,y=0)

frame_alpr = tk.LabelFrame(root, text="", width=250, height=250, font=('times', 14, 'bold'), bg="#87CEEB")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=100, y=300)

entry_label = tk.Label(frame_alpr, text='Enter City:')
entry_label.grid(row=0, column=0, padx=10, pady=10)

city_entry = tk.Entry(frame_alpr)
city_entry.grid(row=0, column=1, padx=10, pady=10)

fetch_button = tk.Button(frame_alpr, text="Fetch Hourly Forecast", command=lambda: fetch_hourly_forecast(city_entry.get()))
fetch_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a Text widget for displaying forecast data
weather_text = tk.Text(root, width=100, height=30, wrap=tk.WORD, bg='white')
weather_text.grid(row=0, column=1, padx=600, pady=200)

# Create a vertical scrollbar and connect it to the Text widget
scrollbar = tk.Scrollbar(root, command=weather_text.yview)
scrollbar.grid(row=0, column=2, sticky='ns')
weather_text.config(yscrollcommand=scrollbar.set)

# Set window dimensions and position
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Run the Tkinter event loop
root.mainloop()
