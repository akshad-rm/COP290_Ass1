from flask import Flask, render_template, request, redirect, url_for
from jugaad_data.nse import NSELive
app = Flask(__name__)

d = {
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

stocksi = {
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


n = NSELive()
stocks=[]
for x in d:
    q= n.stock_quote(d[x])
    d1 = {}
    d1["symbol"] = d[x]
    d1["name"] = x
    d1["price"] = q["priceInfo"]["lastPrice"]
    stocks.append(d1)


# Sample user account data
user_account = {'investments': {}, 'stocks': {}}


@app.route('/')
def home():
    total_investment = sum(user_account['investments'].values())
    return render_template('index.html', stocks=stocks, user_account=user_account, total_investment=total_investment)


@app.route('/buy', methods=['POST'])
def buy_stock():
    symbol = request.form.get('symbol')
    quantity = int(request.form.get('quantity'))

    stock = next((s for s in stocks if s['symbol'] == symbol), None)
    if stock:
        # Update the investments
        investment = stock['price'] * quantity
        if symbol in user_account['investments']:
            user_account['investments'][symbol] += investment
        else:
            user_account['investments'][symbol] = investment

        # Add or update the stock in the user's portfolio
        if symbol in user_account['stocks']:
            user_account['stocks'][symbol] += quantity
        else:
            user_account['stocks'][symbol] = quantity

    return redirect(url_for('home'))


@app.route('/sell', methods=['POST'])
def sell_stock():
    symbol = request.form.get('symbol')
    quantity = int(request.form.get('quantity'))

    if symbol in user_account['stocks'] and user_account['stocks'][symbol] >= quantity:
        # Subtract the sold quantity from the user's portfolio
        user_account['stocks'][symbol] -= quantity

        # Update the investments accordingly
        investment = stocks[stocksi[symbol]]['price'] * quantity
        user_account['investments'][symbol] -= investment

        # Remove the stock from the portfolio if the quantity becomes zero
        if user_account['stocks'][symbol] == 0:
            del user_account['stocks'][symbol]
            del user_account['investments'][symbol]

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
