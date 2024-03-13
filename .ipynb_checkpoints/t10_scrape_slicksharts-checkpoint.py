import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
import os


def get_symbolss_tickers():
        # Scrape 3 indexes from slickcharrs        
        symbolss_ndx = ['sp500','nasdaq100','dowjones']
        for ndx in symbolss_ndx:
            url= f'https://www.slickcharts.com/{ndx}'  # url to scrape
            headers= {'User-Agent': 'Mozilla/5.0'}     # header parameter of the browser
            response = requests.get(url,headers=headers) # response contains data from the requests
            soup = BeautifulSoup(response.text, features="lxml")  # copy text of response to Beautiful soup
            
            # Beautiful soup parses html data
            table = soup.find('table')  # Find the table
            header = []                 # Init header list
            rows = []                   # Init rows
            # Iterate through all the table rows from HTML table
            # First row is the header
            for i, row in enumerate(table.find_all('tr')):
                if i == 0:
                    header = [el.text.strip() for el in row.find_all('th')]
                else:
                    rows.append([el.text.strip() for el in row.find_all('td')])
            
            # Copy the rows and header into the pandas dataframe
            tickers = pd.DataFrame(rows, columns=header)
            # Rename symbols with . to -
            tickers['Symbol'] = tickers['Symbol'].replace('BF.B', 'BF-B')
            tickers['Symbol'] = tickers['Symbol'].replace('BRK.B', 'BRK-B')


            # Check if the folder exists, create it if it does not
            data_path = "data/tickers"
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            # Save to csvfile                   
            TickersFile = f"{data_path}/symbols_{ndx}.csv"
            tickers.to_csv(TickersFile, index=False)           
            
            ticker_list = tickers['Symbol'].tolist()

        # Read 3 CSV files
        df1 = pd.read_csv(f"data/tickers/symbols_sp500.csv")
        df2 = pd.read_csv(f"data/tickers/symbols_nasdaq100.csv")
        df3 = pd.read_csv(f"data/tickers/symbols_dowjones.csv")   

        # Concatenate 'Symbol' columns from all dataframes
        combined_symbols = pd.concat([df1['Symbol'], df2['Symbol'], df3['Symbol']])

        # Remove duplicates
        unique_symbols = combined_symbols.drop_duplicates().reset_index(drop=True)
        unique_symbols.to_csv(f"data/tickers/symbols_all.csv")

        return unique_symbols


def main():
     symbols = get_symbolss_tickers()


main()     
        