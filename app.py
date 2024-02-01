from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as px
from datetime import date,datetime,timedelta
from jugaad_data.nse import stock_df,NSELive
import pandas as pd
import yfinance as yf
from sqlalchemy.orm import relationship
from flask_migrate import Migrate 
import filter_definitions

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Replace with your actual secret key


#---------------Map----------------------------------------------------
company_symbol_map = {
    "Adani Enterprises Ltd.": "ADANIENT",
    "Adani Ports and Special Economic Zone Ltd.": "ADANIPORTS",
    "Apollo Hospitals Enterprise Ltd.": "APOLLOHOSP",
    "Asian Paints Ltd.": "ASIANPAINT",
    "Axis Bank Ltd.": "AXISBANK",
    "Bajaj Auto Ltd.": "BAJAJ-AUTO",
    "Bajaj Finance Ltd.": "BAJFINANCE",
    "Bajaj Finserv Ltd.": "BAJAJFINSV",
    "Bharat Petroleum Corporation Ltd.": "BPCL",
    "Bharti Airtel Ltd.": "BHARTIARTL",
    "Britannia Industries Ltd.": "BRITANNIA",
    "Cipla Ltd.": "CIPLA",
    "Coal India Ltd.": "COALINDIA",
    "Divi's Laboratories Ltd.": "DIVISLAB",
    "Dr. Reddy's Laboratories Ltd.": "DRREDDY",
    "Eicher Motors Ltd.": "EICHERMOT",
    "Grasim Industries Ltd.": "GRASIM",
    "HCL Technologies Ltd.": "HCLTECH",
    "HDFC Bank Ltd.": "HDFCBANK",
    "HDFC Life Insurance Company Ltd.": "HDFCLIFE",
    "Hero MotoCorp Ltd.": "HEROMOTOCO",
    "Hindalco Industries Ltd.": "HINDALCO",
    "Hindustan Unilever Ltd.": "HINDUNILVR",
    "ICICI Bank Ltd.": "ICICIBANK",
    "ITC Ltd.": "ITC",
    "IndusInd Bank Ltd.": "INDUSINDBK",
    "Infosys Ltd.": "INFY",
    "JSW Steel Ltd.": "JSWSTEEL",
    "Kotak Mahindra Bank Ltd.": "KOTAKBANK",
    "L&T Finance Holdings Limited": "LTIM",
    "Larsen & Toubro Ltd.": "LT",
    "Maruti Suzuki India Ltd.": "MARUTI",
    "NTPC Ltd.": "NTPC",
    "Nestle India Ltd.": "NESTLEIND",
    "Oil & Natural Gas Corporation Ltd.": "ONGC",
    "Power Grid Corporation of India Ltd.": "POWERGRID",
    "Reliance Industries Ltd.": "RELIANCE",
    "SBI Life Insurance Company Ltd.": "SBILIFE",
    "State Bank of India": "SBIN",
    "Sun Pharmaceutical Industries Ltd.": "SUNPHARMA",
    "Tata Consultancy Services Ltd.": "TCS",
    "Tata Consumer Products Ltd.": "TATACONSUM",
    "Tata Motors Ltd.": "TATAMOTORS",
    "Tata Steel Ltd.": "TATASTEEL",
    "Tech Mahindra Ltd.": "TECHM",
    "Titan Company Ltd.": "TITAN",
    "UPL Ltd.": "UPL",
    "UltraTech Cement Ltd.": "ULTRACEMCO",
    "Wipro Ltd.": "WIPRO"
}

#--------------------------------------------------------------------


#---------------yfinance Map----------------------------------------------------
yf_map = {
    "Adani Enterprises Limited"  :  "ADANIENT.NS" ,
    "Adani Ports and Special Economic Zone Limited"  :  "ADANIPORTS.NS" ,
    "Apollo Hospitals Enterprise Limited"  :  "APOLLOHOSP.NS" ,
    "Asian Paints Limited"  :  "ASIANPAINT.NS" ,
    "Axis Bank Limited"  :  "AXISBANK.NS" ,
    "Bajaj Auto Limited"  :  "BAJAJ-AUTO.NS" ,
    "Bajaj Finance Limited"  :  "BAJFINANCE.NS" ,
    "Bajaj Finserv Ltd."  :  "BAJAJFINSV.NS" ,
    "Bharat Petroleum Corporation Limited"  :  "BPCL.NS" ,
    "Bharti Airtel Limited"  :  "BHARTIARTL.NS" ,
    "Britannia Industries Limited"  :  "BRITANNIA.NS" ,
    "Cipla Limited"  :  "CIPLA.NS" ,
    "Coal India Limited"  :  "COALINDIA.NS" ,
    "Divi's Laboratories Limited"  :  "DIVISLAB.NS" ,
    "Dr. Reddy's Laboratories Limited"  :  "DRREDDY.NS" ,
    "Eicher Motors Limited"  :  "EICHERMOT.NS" ,
    "Grasim Industries Limited"  :  "GRASIM.NS" ,
    "HCL Technologies Limited"  :  "HCLTECH.NS" ,
    "HDFC Bank Limited"  :  "HDFCBANK.NS" ,
    "HDFC Life Insurance Company Limited"  :  "HDFCLIFE.NS" ,
    "Hero MotoCorp Limited"  :  "HEROMOTOCO.NS" ,
    "Hindalco Industries Limited"  :  "HINDALCO.NS" ,
    "Hindustan Unilever Limited"  :  "HINDUNILVR.NS" ,
    "ICICI Bank Limited"  :  "ICICIBANK.NS" ,
    "ITC Limited"  :  "ITC.NS" ,
    "IndusInd Bank Limited"  :  "INDUSINDBK.NS" ,
    "Infosys Limited"  :  "INFY.NS" ,
    "JSW Steel Limited"  :  "JSWSTEEL.NS" ,
    "Kotak Mahindra Bank Limited"  :  "KOTAKBANK.NS" ,
    "LTIMindtree Limited"  :  "LTIM.NS" ,
    "Larsen & Toubro Limited"  :  "LT.NS" ,
    "Maruti Suzuki India Limited"  :  "MARUTI.NS" ,
    "NTPC Limited"  :  "NTPC.NS" ,
    "Nestlé India Limited"  :  "NESTLEIND.NS" ,
    "Oil and Natural Gas Corporation Limited"  :  "ONGC.NS" ,
    "Power Grid Corporation of India Limited"  :  "POWERGRID.NS" ,
    "Reliance Industries Limited"  :  "RELIANCE.NS" ,
    "SBI Life Insurance Company Limited"  :  "SBILIFE.NS" ,
    "State Bank of India"  :  "SBIN.NS" ,
    "Sun Pharmaceutical Industries Limited"  :  "SUNPHARMA.NS" ,
    "Tata Consultancy Services Limited"  :  "TCS.NS" ,
    "Tata Consumer Products Limited"  :  "TATACONSUM.NS" ,
    "Tata Motors Limited"  :  "TATAMOTORS.NS" ,
    "Tata Steel Limited"  :  "TATASTEEL.NS" ,
    "Tech Mahindra Limited"  :  "TECHM.NS" ,
    "Titan Company Limited"  :  "TITAN.NS" ,
    "UPL Limited"  :  "UPL.NS" ,
    "UltraTech Cement Limited"  :  "ULTRACEMCO.NS" ,
    "Wipro Limited"  :  "WIPRO.NS" 
}


#--------------------------------------------------------------------

#---------------stock index map----------------------------------------------------
stocks_index = {
    'ADANIENT': 0,
    'ADANIPORTS': 1,
    'APOLLOHOSP': 2,
    'ASIANPAINT': 3,
    'AXISBANK': 4,
    'BAJAJ-AUTO': 5,
    'BAJFINANCE': 6,
    'BAJAJFINSV': 7,
    'BPCL': 8,
    'BHARTIARTL': 9,
    'BRITANNIA': 10,
    'CIPLA': 11,
    'COALINDIA': 12,
    'DIVISLAB': 13,
    'DRREDDY': 14,
    'EICHERMOT': 15,
    'GRASIM': 16,
    'HCLTECH': 17,
    'HDFCBANK': 18,
    'HDFCLIFE': 19,
    'HEROMOTOCO': 20,
    'HINDALCO': 21,
    'HINDUNILVR': 22,
    'ICICIBANK': 23,
    'ITC': 24,
    'INDUSINDBK': 25,
    'INFY': 26,
    'JSWSTEEL': 27,
    'KOTAKBANK': 28,
    'LTIM': 29,
    'LT': 30,
    'MARUTI': 31,
    'NTPC': 32,
    'NESTLEIND': 33,
    'ONGC': 34,
    'POWERGRID': 35,
    'RELIANCE': 36,
    'SBILIFE': 37,
    'SBIN': 38,
    'SUNPHARMA': 39,
    'TCS': 40,
    'TATACONSUM': 41,
    'TATAMOTORS': 42,
    'TATASTEEL': 43,
    'TECHM': 44,
    'TITAN': 45,
    'UPL': 46,
    'ULTRACEMCO': 47,
    'WIPRO': 48
}

#--------------------------------------------------------------------


#-----------------------feeding live data----------------------------
nse_data_obj = NSELive()
company_stocks=[]
company_plots =[]
for company in company_symbol_map:
    quote = nse_data_obj.stock_quote(company_symbol_map[company])
    temp_dict = {}
    temp_dict["symbol"] = company_symbol_map[company]
    temp_dict["name"] = company
    temp_dict["price"] = quote["priceInfo"]["lastPrice"]
    temp_dict["change"] = quote["priceInfo"]["change"]
    temp_dict["pchange"] = quote["priceInfo"]["pChange"]
    company_stocks.append(temp_dict)
#---------------------------------------------------------------------


# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# User Model
class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    investments = db.relationship('Investment', backref='user', lazy=True)
    stocks = db.relationship('Stock', backref='user', lazy=True)


# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('index'))
    



@app.route('/explore')
def explore():
    return render_template('explore.html',username=session['username'])   



@app.route('/history_analysis')
def history_analysis():
    return render_template('history_analysis.html',username=session['username'])  


@app.route('/filters')
def filters():
    return render_template('filters.html',username=session['username'])



@app.route('/intermediate_filter',methods = ['POST'])
def intermediate_filter():
    if request.method=='POST':
        filters_selected = request.form.getlist("filter_category")
        PE_filter = 0
        avg_price = 0
        market_cap = 0
        sectors_selected = []
        filtered_companies = []
        first_filter_flag = 0
        if "PE_ratio" in filters_selected:
            PE_filter = request.form.get("PE_ratio")
            if first_filter_flag==0:
                filtered_companies = filter_definitions.filter_by_pe(PE_filter)
                first_filter_flag = 1
            else :
                temp_list = filter_definitions.filter_by_pe(PE_filter)
                filtered_companies = [value for value in temp_list if value in filtered_companies]

        if "Avg_price" in filters_selected:
            avg_price = request.form.get("Avg_price")
            if first_filter_flag==0:
                filtered_companies = filter_definitions.filter_by_avg(avg_price)
                first_filter_flag = 1
            else:
                temp_list = filter_definitions.filter_by_avg(avg_price)
                filtered_companies = [value for value in temp_list if value in filtered_companies]

        if "Market_cap" in filters_selected:
            market_cap = request.form.get("Market_cap")
            if first_filter_flag==0:
                filtered_companies = filter_definitions.filter_by_mc(market_cap)
                first_filter_flag=1
            else:
                temp_list = filter_definitions.filter_by_mc(market_cap)
                filtered_companies = [value for value in temp_list if value in filtered_companies]


        if "selected_sector" in filters_selected:
            sectors_selected = request.form.getlist("selected_sector")
            if first_filter_flag==0:
                filtered_companies = filter_definitions.filter_by_sector(sectors_selected)
                first_filter_flag=1
            else:
                temp_list = filter_definitions.filter_by_sector(sectors_selected)
                filtered_companies = [value for value in temp_list if value in filtered_companies]

        if first_filter_flag==0:
            return redirect(url_for('filters'))
        filtered_companies_data = []
        company_data = []
        current_date = date.today().strftime('%Y-%m-%d')
        for filtered_company in filtered_companies:
            symbol = yf_map[filtered_company]
            stock = yf.Ticker(symbol)
            info = stock.info
            history = stock.history(start=current_date)  
            average_price = history['Close'].mean()
            filtered_companies_data.append({
                'Symbol': symbol,
                'Company_Name': info.get('longName', ''),
                'Sector': info.get('industry', ''),
                'Market_Cap': info.get('marketCap', ''),
                'Previous_Close': info.get('regularMarketPreviousClose', ''),
                'PE_Ratio': info.get('trailingPE', ''),
                'Monthly_avg': average_price,
            })


        
        return render_template('result_filter.html',filtered_companies_data = filtered_companies_data)



    else:
        return redirect(url_for('filters'))


@app.route('/intermediate',methods = ['POST'])
def intermediate():
    if request.method == 'POST':
        companies = request.form.getlist("company")
        
        from_date_str = request.form.get('fromDate')
        to_date_str = request.form.get('toDate')
        category = request.form.get('category')
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
        df_array=  []
        categories_needed = ["DATE","SYMBOL"]
        categories_needed.append(category)
        for company in companies :
            respective_symbol = company_symbol_map[company]
            df_temp = stock_df(symbol=respective_symbol,from_date=from_date,to_date=to_date,series = "EQ")
            df_needed = df_temp[categories_needed]
            df_array.append(df_needed)
        
        df_complete = pd.concat(df_array)
        fig = px.line(df_complete, x='DATE', y=category, color='SYMBOL', line_group='SYMBOL',
              title='Multiple Line Graphs for Different Categories')
        fig.update_layout(template= 'plotly_dark')
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ]),
                    
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        plot_html = fig.to_html(full_html = False)
        
        return render_template('result_plot.html', plot_html=plot_html)
    else:
        return redirect(url_for('explore'))
    



@app.route('/transactions')
def transactions():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        total_investment = sum(investment.amount for investment in user.investments)
        return render_template('trading.html', stocks=company_stocks, user_account=user, total_investment=total_investment)
    else:
        return redirect(url_for('login'))






@app.route('/buy', methods=['POST'])
def buy_stock():
    user = User.query.get(session['user_id'])
    symbol = request.form.get('symbol')
    quantity = int(request.form.get('quantity'))

    stock = next((s for s in company_stocks if s['symbol'] == symbol), None)
    if stock:
        investment_amount = stock['price'] * quantity
        investment = Investment(symbol=symbol, amount=investment_amount, user_id=user.id)
        db.session.add(investment)
        db.session.commit()

        user_stock = Stock.query.filter_by(symbol=symbol, user_id=user.id).first()
        if user_stock:
            user_stock.quantity += quantity
            user_stock.amount += investment_amount
        else:
            user_stock = Stock(symbol=symbol, quantity=quantity,amount=investment_amount, user_id=user.id)
            db.session.add(user_stock)
        db.session.commit()

    return redirect(url_for('transactions'))

@app.route('/sell', methods=['POST'])
def sell_stock():
    symbol = request.form.get('symbol')
    quantity = int(request.form.get('quantity'))
    user = User.query.get(session['user_id'])

    user_stock = Stock.query.filter_by(symbol=symbol, user_id=user.id).first()
    if user_stock and user_stock.quantity >= quantity:
        user_stock.quantity -= quantity
        db.session.commit()

        investment_amount = company_stocks[stocks_index[symbol]]['price'] * quantity
        user_stock.amount -= investment_amount
        investment = Investment(symbol=symbol, amount=-investment_amount, user_id=user.id)
        db.session.add(investment)
        db.session.commit()

        if user_stock.quantity == 0:
            db.session.delete(user_stock)
            db.session.commit()

    return redirect(url_for('transactions'))



@app.route('/live_data')
def live_data():

    return render_template('live_data.html',companies = company_stocks)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)





