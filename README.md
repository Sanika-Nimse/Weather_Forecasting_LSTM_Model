
# Weather Forecasting using Spatial Feature Based LSTM Model

This repository contains the implementation of a **Short-Term Weather Forecasting Model** that leverages **Spatial Feature Attention** with an LSTM architecture. The model has been rigorously tested and validated, achieving an accuracy of **89%** for 48-hour weather forecasts.

## Overview

- Developed a **Short-Term Weather Forecasting Model** using **Spatial Feature Attention** to enhance prediction accuracy.
- The model utilizes **Python** and various **Deep Learning libraries** for pre-processing meteorological data, training the LSTM model, and implementing the attention mechanism.
- Achieved **89% accuracy** in predicting short-term weather forecasts (up to 48 hours).

## Features

- **Spatial Feature Attention**: Integrates spatial features to improve the forecast model's performance.
- **LSTM Architecture**: Uses Long Short-Term Memory (LSTM) networks, which are well-suited for time series forecasting.
- **Meteorological Data Preprocessing**: Implements effective data preprocessing techniques for handling large weather datasets.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-forecast-lstm.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Download the dataset from [your dataset source] and place it in the `data/` folder.
2. Pre-process the data using the provided scripts:
   ```bash
   python preprocess_data.py
   ```
3. Train the LSTM model:
   ```bash
   python train_model.py
   ```
4. Evaluate the model:
   ```bash
   python evaluate_model.py
   ```

## Results

- The model has achieved an **89% accuracy** for 48-hour weather forecasts.
- Thorough testing and validation were performed using real-world meteorological datasets.

## Dependencies

- **Python 3.x**
- **TensorFlow**
- **Keras**
- **NumPy**
- **Pandas**
- **Matplotlib**

## Contributing

Contributions are welcome! Please feel free to open a pull request or submit an issue if you encounter any bugs or have feature requests.
