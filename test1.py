import yfinance as yf
from datetime import date


nifty_50_symbols =['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS', 'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS', 'LT.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']
company_data = []
current_date = date.today().strftime('%Y-%m-%d')
for symbol in nifty_50_symbols:
    stock = yf.Ticker(symbol)
    info = stock.info
    history = stock.history(start=current_date)  
    average_price = history['Close'].mean()
    company_data.append({
        'Symbol': symbol,
        'Company_Name': info.get('longName', ''),
        'Sector': info.get('industry', ''),
        'Market_Cap': info.get('marketCap', ''),
        'Previous_Close': info.get('regularMarketPreviousClose', ''),
        'PE_Ratio': info.get('trailingPE', ''),
        'Monthly_avg': average_price,
        
    })
    print("\"",info.get('longName',''),"\""," : ","\"",symbol,"\"",",")

