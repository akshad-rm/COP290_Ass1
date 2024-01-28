from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as px
from datetime import date,datetime,timedelta
from jugaad_data.nse import stock_df
import pandas as pd

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
    "LTIMindtree Ltd.": "LTIM",
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

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    else :
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
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        #fig.show()
        plot_html = fig.to_html(full_html = False)
        
        return render_template('result_plot.html', plot_html=plot_html)
    else:
        return redirect(url_for('explore'))
    


# @app.route('/result_plot')
# def result_plot():
#     plot_html = session.pop('plot_html', None)
#     if plot_html:
#         return render_template('result_plot.html', plot_html=plot_html)
#     else:
#         return "Plot HTML not found in session."

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)





