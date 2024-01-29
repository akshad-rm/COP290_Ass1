import yfinance as yf
import pandas as pd
from datetime import date

text = """Thermal Coal
Marine Shipping
Medical Care Facilities
Specialty Chemicals
Banks - Regional
Auto Manufacturers
Credit Services
Financial Conglomerates
Oil & Gas Refining & Marketing
Telecom Services
Packaged Foods
Drug Manufacturers - General
Thermal Coal
Drug Manufacturers - Specialty & Generic
Drug Manufacturers - Specialty & Generic
Auto Manufacturers
Building Materials
Information Technology Services
Banks - Regional
Insurance - Life
Auto Manufacturers
Aluminum
Household & Personal Products
Banks - Regional
Tobacco
Banks - Regional
Information Technology Services
Steel
Banks - Regional
Information Technology Services
Engineering & Construction
Auto Manufacturers
Utilities - Regulated Electric
Packaged Foods
Oil & Gas Integrated
Utilities - Regulated Electric
Oil & Gas Refining & Marketing
Insurance - Life
Banks - Regional
Drug Manufacturers - Specialty & Generic
Information Technology Services
Packaged Foods
Auto Manufacturers
Steel
Information Technology Services
Luxury Goods
Agricultural Inputs
Building Materials
Information Technology Services"""

# Split the text by line breaks and remove empty lines
sec = [line.strip() for line in text.split('\n') if line.strip()]
