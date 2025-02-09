from imports import pd, source, time, np, datetime

data_points = ['symbol', 'shortName', 'currency', 'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose',
               'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh', 'dividendRate', 'dividendYield',
              'fiveYearAvgDividendYield', 'beta', 'trailingPE', 'forwardPE', 'volume',  'marketCap',
              'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months', 'fiftyDayAverage', 
              'twoHundredDayAverage', 'profitMargins', 'bookValue', 'priceToBook', 'earningsQuarterlyGrowth', 
              'netIncomeToCommon', 'trailingEps', 'forwardEps', 'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange',
              'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 
              'returnOnEquity', 'grossProfits', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 
              'ebitdaMargins', 'operatingMargins', 'trailingPegRatio']

def formatDatatoFile(data:list[list]):
    '''
    This function formats the data fetched from the API and saves it to a csv file.
    It does data cleaning and formatting.
    
    **Arguments**:
            data: Data fetched in list format from each company.
    '''
    stocksData_df = pd.DataFrame(data, columns=data_points)
    stocksData_df = stocksData_df.dropna(subset=["symbol"])
    stocksData_df = stocksData_df.replace([np.nan], 0.0)
    stocksData_df.columns = [i.capitalize() for i in stocksData_df.columns]
    stocksData_df['Marketcap'] = stocksData_df['Marketcap']/(10e8) # Converting marketcap in order of 100 million
    stocksData_df['Returnonequity'] = stocksData_df['Returnonequity']*100 # Converting to percentage
    stocksData_df['Earningsgrowth'] = stocksData_df['Earningsgrowth']*100 # Converting to percentage
    stocksData_df['Revenuegrowth'] = stocksData_df['Revenuegrowth']*100 # Converting to percentage
    stocksData_df['Profitmargins'] = stocksData_df['Profitmargins']*100 # Converting to percentage
    stocksData_df['Ebitdamargins'] = stocksData_df['Ebitdamargins']*100 # Converting to percentage
    stocksData_df['Totalrevenue'] = stocksData_df['Totalrevenue']/(10e8) # Converting total revenue in order of 100 million
    stocksData_df['Grossprofits'] = stocksData_df['Grossprofits']/(10e8) # Converting gross profits in order of 100 million
    stocksData_df['Freecashflow'] = stocksData_df['Freecashflow']/(10e8) # Converting free cash flow in order of 100 million
    stocksData_df['Operatingcashflow'] = stocksData_df['Operatingcashflow']/(10e8) # Converting free cash flow in order of 100 million
    stocksData_df = stocksData_df[stocksData_df['Currency']!='0.0']
    stocksData_df = stocksData_df.round(2)
    # Drop duplicates based on the Symbol column, keeping the first occurrence
    stocksData_df = stocksData_df.drop_duplicates(subset="Symbol", keep="first")
    stocksData_df.reset_index(drop=True, inplace=True)

    stocksData_df.to_csv("stocksData.csv", index=False)
    print("Saved data to csv file.")


def download_data(stocks):
    '''
        **Arguments**:
            stocks: List of stock tickers to download data for
    '''
    data = []
    stk = source.Tickers(" ".join(stocks))
    for ticker in stocks:
        try:
            stock_info = stk.tickers[ticker].info
            row = {key: stock_info.get(key, None) for key in data_points}
            data.append(row)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    print(f"Done fetching data for {len(data)} stocks.")
    
    # The data we need :- 
    stocksData = [i for i in data if i!=None]
    formatDatatoFile(stocksData)
    
    
def fetchTickers():
    '''
    Fetches the list of NASDAQ-listed companies with the ticker symbol, company name, and more information.
        
    **Returns**: List of NASDAQ-listed companies with the ticker symbol and company name.
    '''
    # URLs for the NASDAQ Trader Symbol Directory files
    # List is updated everyday.
    nasdaq_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"

    # Load NASDAQ-listed stocks
    nasdaq_data = pd.read_csv(nasdaq_url, sep="|")
    # Remove the last row (footer info)
    nasdaq_data = nasdaq_data[:-1]

    #  Filter for companies that are not bankrupt, delisted, etc.
    normal_cmps = nasdaq_data.where(nasdaq_data["Financial Status"] == "N").dropna()
    normal_cmps.index = range(len(normal_cmps))
    nasdaq_tickers = normal_cmps[["Symbol", "Security Name"]]
    nasdaq_tickers.loc[:, "Exchange"] = "NASDAQ"
    return nasdaq_tickers


def main():
    batch_size = 25
    nasdaq_tickers = fetchTickers()
    m = len(list(nasdaq_tickers["Symbol"]))

    for idx in range(0, m, batch_size):
        download_data(list(nasdaq_tickers["Symbol"][idx:idx+batch_size]))
        time.sleep(4) 

if __name__ == "__main__":
    main()
    # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")