import pandas as pd
import yfinance as yf
from datetime import date



high_to_sub_sector_map = {
    "Energy & Utilities": ["Thermal Coal", "Oil & Gas Refining & Marketing", "Oil & Gas Integrated", "Utilities - Regulated Electric"],
    "Transportation": ["Marine Shipping", "Auto Manufacturers"],
    "Healthcare": ["Medical Care Facilities", "Drug Manufacturers - General"],
    "Financial Services": ["Banks - Regional", "Credit Services", "Financial Conglomerates"],
    "Chemicals": ["Specialty Chemicals"],
    "Technology": ["Information Technology Services"],
    "Food & Consumer Goods": ["Packaged Foods", "Household & Personal Products", "Tobacco", "Luxury Goods"],
    "Metals & Construction": ["Aluminum", "Steel", "Building Materials", "Engineering & Construction"],
    "Telecommunications": ["Telecom Services"],
    "Pharmaceuticals & Agriculture": ["Drug Manufacturers - Specialty & Generic", "Agricultural Inputs"]
}





def get_nifty_50_data():

    nifty_50_symbols =['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS', 'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS', 'LT.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']
    company_data = []
    current_date = date(2024,1,26).strftime('%Y-%m-%d')

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

    return company_data


nifty_50_data = get_nifty_50_data()

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(nifty_50_data)
df.at[43,"PE_Ratio"] = "-26.3"
df["PE_Ratio"] = df["PE_Ratio"].astype(float)
# Display the DataFrame

def filter_by_pe(x):
    s = "PE_Ratio >" + str(x)
    df_pe = df.query(s)
    l = df_pe["Company_Name"].tolist()
    return l

def filter_by_mc(x):
    s = "Market_Cap >" + str(x)
    df_mc = df.query(s)
    l = df_mc["Company_Name"].tolist()
    return l

def filter_by_avg(x):
    s = "Monthly_avg >" + str(x)
    df_avg = df.query(s)
    l = df_avg["Company_Name"].tolist()
    return l

def filter_by_sector(arr):
    arr1 = []
    for high_sector in arr:
        arr1 = arr1 + high_to_sub_sector_map[high_sector]
    df_sector = pd.DataFrame()
    for x in arr1:
        s = "Sector == '" + x + "'"
        df_sector = pd.concat([df_sector,df.query(s)])
    l = df_sector["Company_Name"].tolist()
    return l