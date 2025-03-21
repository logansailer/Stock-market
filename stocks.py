from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import config

def main():
    data_source = 'alphavantage'
    df = readData(data_source)
    plotData(df)


def readData(data_source):
    if data_source == 'alphavantage':
        print("<====== Loading Data ======>")

        api_key = config.API_KEY # gets API key from config file
        
        ticker = "AAL"  # American Airlines stock market

        #json file with all the stock market data
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)

        #save the data to a file
        file_to_save = f"stock_market_data-{ticker}.csv"
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data = json.loads(url.read().decode())

                #get needed data from json and saves it to csv
                data = data["Time Series (Daily)"]
                df = pd.DataFrame(columns=["Date", "Low", "High", "Close", "Open"])
                for k, v in data.items():
                    date = dt.datetime.strptime(k, "%Y-%m-%d")
                    data_row = [date.date(), float(v["3. low"]), float(v["2. high"]), float(v["4. close"]), float(v["1. open"])]
                    df.loc[-1, :] = data_row
                    df.index = df.index +1
            print(f"Data saved to : {file_to_save}")
            df.to_csv(file_to_save)
        
        else:
            print("File already exists. Loading data...")
            df = pd.read_csv(file_to_save)
        
        #sort data by date
        df = df.sort_values("Date")
        df.head()
        return df

def plotData(df):
    plt.figure(figsize = (18,9))
    plt.plot(range(df.shape[0]), (df["Low"]+df["High"])/2.0)
    plt.xticks(range(0, df.shape[0], 500), df["Date"].loc[::500], rotation = 45)
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Mid Price", fontsize=18)
    plt.show()

if __name__ == "__main__":
    main()