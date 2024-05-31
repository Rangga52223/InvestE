import yfinance as yf
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import os
from datetime import datetime

def proses_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    target_y = stock_data['Close']
    X_feat = stock_data.iloc[:, 0:3]  # Menggunakan kolom Open, High, Low
    sc = StandardScaler()
    X_ft = sc.fit_transform(X_feat.values)
    X_ft = pd.DataFrame(columns=X_feat.columns, data=X_ft, index=X_feat.index)
    return X_ft, target_y, sc

def lstm_split(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i + n_steps, :])
        y.append(data[i + n_steps, -1])
    return np.array(X), np.array(y)

def data_latih(X_ft, target_y):
    n_steps = 10
    X1, y1 = lstm_split(X_ft.values, n_steps)
    train_size = int(len(X_ft) * 0.8)
    X_train, X_test = X1[:train_size], X1[train_size:]
    y_train, y_test = y1[:train_size], y1[train_size:]
    return X_train, X_test, y_train, y_test, n_steps

def lstm(X_train, y_train, n_steps):
    model = Sequential()
    model.add(LSTM(32, input_shape=(n_steps, X_train.shape[2]), activation='relu', return_sequences=False))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, epochs=100, batch_size=16, verbose=2, shuffle=False)
    return model

def load_existing_model(model_path):
    if os.path.exists(model_path):
        return load_model(model_path)
    return None

def prediksi_berulang(model, X_test, n_steps, pred_days, sc):
    predictions = []
    current_batch = X_test[-1]  # Mulai dari batch terakhir data uji
    for _ in range(pred_days):
        current_pred = model.predict(current_batch.reshape(1, n_steps, current_batch.shape[1]))
        predictions.append(current_pred[0][0])
        # Update current_batch dengan prediksi baru di kolom Close
        new_row = np.append(current_batch[-1, :-1], current_pred[0][0])
        current_batch = np.append(current_batch[1:], [new_row], axis=0)

    # Balikkan normalisasi
    predictions = np.array(predictions).reshape(-1, 1)
    predictions = sc.inverse_transform(np.concatenate((np.zeros((predictions.shape[0], 2)), predictions), axis=1))[:, -1]

    # Bulatkan hasil prediksi ke dua tempat desimal
    predictions = np.round(predictions, 2)
    return predictions.tolist()

def hitung_rmse(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    return rmse, y_test

def prediksi(ticker, start_date, end_date, pred_days=7):
    model_dir = r'/InvestE/model'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_path = os.path.join(model_dir, f"{ticker}.h5")
    
    X_ft, target_y, sc = proses_data(ticker, start_date, end_date)
    X_train, X_test, y_train, y_test, n_steps = data_latih(X_ft, target_y)

    model = load_existing_model(model_path)
    if model is None:
        model = lstm(X_train, y_train, n_steps)
        model.save(model_path)

    rmse, y_test = hitung_rmse(model, X_test, y_test)
    mean_actual_prices = np.mean(y_test)
    relative_error = rmse / mean_actual_prices
    accuracy = (1 - relative_error) * 100
    predictions = prediksi_berulang(model, X_test, n_steps, pred_days, sc)
    
    return predictions, rmse, accuracy