import yfinance as yf
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

def proses_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    target_y = stock_data['Close']
    X_feat = stock_data.iloc[:, 0:3]  # Menggunakan kolom Open, High, Low
    global sc
    sc = StandardScaler()
    X_ft = sc.fit_transform(X_feat.values)
    X_ft = pd.DataFrame(columns=X_feat.columns, data=X_ft, index=X_feat.index)
    return X_ft, target_y

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

def prediksi(ticker, start_date, end_date):
    X_ft, target_y = proses_data(ticker, start_date, end_date)
    X_train, X_test, y_train, y_test, n_steps = data_latih(X_ft, target_y)
    model = lstm(X_train, y_train, n_steps)
    predictions = model.predict(X_test)
    return predictions.tolist(), y_test.tolist()

# if __name__ == "__main__":
#     ticker = "AAPL"
#     start_date = "2020-01-01"
#     end_date = "2021-01-01"
#     predictions, y_test = prediksi(ticker, start_date, end_date)
    
#     predictions_transformed = sc.inverse_transform(predictions)
#     y_test_transformed = sc.inverse_transform(y_test)

#     print(predictions)
#     print(y_test)
#     print(mean_squared_error(y_test, predictions)**0.5)