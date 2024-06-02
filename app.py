
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
import yfinance as yf
from datetime import datetime, timedelta
from forms import RegistrationForm, LoginForm, StockForm
import ai as prediksi
import ai2 as predi
import os
import uuid
app = Flask(__name__)
app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)
import logging
csp = {
    'default-src': '\'self\'',
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',  # Untuk mengizinkan inline scripts
    ],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',  # Untuk mengizinkan inline styles
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/npm/feather-icons@4.28.0/dist/feather.min.js',  # Ganti dengan URL CDN Anda
        '\'unsafe-inline\'',  # Untuk mengizinkan inline styles jika diperlukan
    ],
    'default-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',  # Bootstrap CDN
        'https://web-chat.global.assistant.watson.appdomain.cloud',  # Watson Assistant Chat CDN
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',  # Bootstrap CDN
        'https://web-chat.global.assistant.watson.appdomain.cloud',  # Watson Assistant Chat CDN
        '\'unsafe-inline\'',  # Untuk mengizinkan inline scripts jika diperlukan
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',  # Bootstrap CDN
        'https://web-chat.global.assistant.watson.appdomain.cloud',  # Watson Assistant Chat CDN
        '\'unsafe-inline\'',  # Untuk mengizinkan inline styles jika diperlukan
    ],
}

talisman = Talisman(
    app,
    content_security_policy=csp
)


# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'invest_e_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Security Configurations
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize Flask-Talisman for secure headers
Talisman(app)


# Global variables for stock data
x = 'BBCA.JK'
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
start_date1 = end_date - timedelta(days=30)

# Stock lists
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

stock_data = yf.download(x, start=start_date, end=end_date)
stock_data1 = yf.download(x, start=start_date1, end=end_date)

# Configure logging
@app.route('/')
# Exempt Talisman for this route
@csrf.exempt
def intro():
    return render_template('landing-page.html')

@app.route('/dashboard', methods=["POST", "GET"])
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt
def home():
    form = StockForm()
    if 'loggedin' in session:
        if request.method == "POST":
            global x, selected_time
            x = request.form["emtn"]
            selected_time = request.form["time"]

            global end_date, start_date
            end_date = datetime.now()
            if selected_time == '3d':
                start_date = end_date - timedelta(days=3)
            elif selected_time == '5d':
                start_date = end_date - timedelta(days=5)
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
                start_date = None  

            global stock_data, stock_data1
            stock_data = yf.download(x, start=start_date, end=end_date)
            if stock_data is None or stock_data.empty:
                flash('Error loading stock data. Please try again.', 'danger')
                return redirect(url_for("home"))
            username = session['username']
            return redirect(url_for("home",username = username))
        else:
            selected_ticker = request.args.get('selected_ticker')
            return render_template('index.html', form=form,watchlist=selected_ticker, indonesian_stocks=indonesian_stocks)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password_hash'], password):
            session['loggedin'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET'])
def register1():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@app.route('/proses_register', methods=['POST'])
def proses_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate a random UUID for the id column
        user_id = str(uuid.uuid4())
        
        # Retrieve form data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        nama = form.nama.data
        pekerjaan = form.pekerjaan.data
        tgl_lahir = form.tgl_lahir.data
        umur = form.umur.data
        
        # Hash the password
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        
        # Execute the INSERT query
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (id, username, email, password_hash, nama, pekerjaan, tgl_lahir_tempat, umur) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (user_id, username, email, hash_password, nama, pekerjaan, tgl_lahir, umur))
        mysql.connection.commit()
        cursor.close()
            
            # Log the registration event
        
            
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)


@app.route('/stock')
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt  # Exempt CSRF token for this route
def stock():
    if 'loggedin' in session:
        username = session['username']
        return render_template('List-Stock.html', indonesian_stocks=indonesian_stocks, us_stocks=us_stocks, username=username)
    return redirect(url_for('login'))

@app.route('/stockdata')
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt  # Exempt CSRF token for this route
def stock_data():
    if 'loggedin' in session:
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
    return redirect(url_for('login'))

@app.route('/data')
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt  # Exempt CSRF token for this route
def get_data():
    if 'loggedin' in session:
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
    return redirect(url_for('login'))

@app.route('/ai')
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt  # Exempt CSRF token for this route
def index():
    if 'loggedin' in session:
        username = session['username']
        return render_template('AI.html', IDstocks=indonesian_stocks, username=username)
    return redirect(url_for('login'))

@app.route('/predict')
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt
def predict():
    ticker = request.args.get('ticker', default='BBCA.Jk', type=str)
    start_date = '2018-01-01'
    end_date = str(datetime.now().date())
    pred_days = 7
    predictions, rmse, accuracy = predi.prediksi(ticker, start_date, end_date, pred_days)
    return jsonify(predictions=predictions, rmse=rmse, accuracy=accuracy)


@app.route('/getdata', methods=["GET"])
@talisman(content_security_policy=None)  # Exempt Talisman for this route
@csrf.exempt
def getdata():
    if 'loggedin' in session:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        filtered_data = stock_data.loc[start_date:end_date]
        data = {
            'emiten': x,
            'dates': filtered_data.index.strftime('%Y-%m-%d').tolist(),
            'close': filtered_data['Close'].tolist(), 
        }
        return jsonify(data)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
