from flask import Flask, render_template, jsonify, request, redirect, url_for
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import ai as prediksi
import ai2 as predi

app = Flask(__name__)

# Download data once and store it in a global DataFrame
x = 'BBCA.JK'
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
start_date1 = end_date - timedelta(days=30)

indonesian_stocks = [
    "BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK",
    "BBNI.JK", "GGRM.JK", "HMSP.JK", "ICBP.JK", "KLBF.JK",
    "PGAS.JK", "PTBA.JK", "SMGR.JK", "UNVR.JK", "WIKA.JK"
]

us_stocks = [
    "AAPL", "ABBV", "AMZN", "BAC",
    "BA", "COST", "CMCSA", "COP",
    "CVX", "DIS", "DUK", "EXC", "GOOGL",
    "GS", "HD", "HON", "JNJ", "JPM"
]

# Global DataFrame to store stock data
stock_data = yf.download(x, start=start_date, end=end_date)
stock_data1 = yf.download(x, start=start_date1, end=end_date)

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        global x, selected_time
        x = request.form["emtn"]
        selected_time = request.form["time"]
        print(x)

        global end_date, start_date
        end_date = datetime.now()
        if selected_time == '3d':
            start_date = end_date - timedelta(days=3)
        elif selected_time == '7d':
            start_date = end_date - timedelta(days=7)
        elif selected_time == '1mo':
            start_date = end_date - timedelta(days=30)
        elif selected_time == '3mo':
            start_date = end_date - timedelta(days=90)
        elif selected_time == '6mo':
            start_date = end_date - timedelta(days=180)
        elif selected_time == '1y':
            start_date = end_date - timedelta(days=365)
        elif selected_time == '5y':
            start_date = end_date - timedelta(days=1825)
        else:
            start_date = None  # Use all available data

        global stock_data, stock_data1
        stock_data = yf.download(x, start=start_date, end=end_date)
        stock_data1 = yf.download(x, start=start_date, end=end_date)
        return redirect(url_for("home"))
    else:
        selected_ticker = request.args.get('selected_ticker')
        return render_template('index.html', watchlist=selected_ticker, indonesian_stocks=indonesian_stocks)


@app.route('/stock')
def stock():
    return render_template('List-Stock.html', indonesian_stocks=indonesian_stocks, us_stocks=us_stocks)

@app.route('/stockdata')
def stock_data():
    data_indo = []
    data_us = []

    for emiten in indonesian_stocks:
        stock = yf.Ticker(emiten)
        hist = stock.history(period="1d")
        if not hist.empty:
            close_price = int(hist['Close'].iloc[0])  
            volume = int(hist['Volume'].iloc[0])     
            data_indo.append({
                "emiten": emiten,
                "close": close_price,
                "volume": volume
            })

    for emiten in us_stocks:
        stock = yf.Ticker(emiten)
        hist = stock.history(period="1d")
        if not hist.empty:
            close_price = int(hist['Close'].iloc[0])  
            volume = int(hist['Volume'].iloc[0])     
            data_us.append({
                "emiten": emiten,
                "close": close_price,
                "volume": volume
            })

    return jsonify(data_indo, data_us)


@app.route('/data')
def get_data():
    data = {
        'emiten' : x,
        'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
        'open': stock_data['Open'].tolist(),
        'high': stock_data['High'].tolist(),
        'low': stock_data['Low'].tolist(),
        'close': stock_data['Close'].tolist(),
        'volume': stock_data['Volume'].tolist()
    }
    return jsonify(data)

@app.route('/ai')
def index():
    return render_template('AI.html', IDstocks=indonesian_stocks)

@app.route('/predict')
def predict():
    ticker = request.args.get('ticker', default='BBCA.jk', type=str)
    start_date = '2018-01-01'
    end_date = str(datetime.now().date())
    pred_days = 7
    predictions, rmse, accuracy = predi.prediksi(ticker, start_date, end_date, pred_days)
    return jsonify(predictions=predictions, rmse=rmse, accuracy=accuracy)

@app.route('/getdata')
def data1():
    # Ambil tanggal awal dan akhir dari parameter start_date dan end_date
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Konversi tanggal awal dan akhir menjadi objek datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # Filter data within the date range
    filtered_data = stock_data1.loc[start_date:end_date]
    
    # Format data untuk dikirim sebagai JSON
    data = {
        'emiten' : x,
        'dates': filtered_data.index.strftime('%Y-%m-%d').tolist(),
        'close': filtered_data['Close'].tolist(),
    }
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
