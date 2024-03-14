import pandas as pd

car_list = ['honda', 'toyota', 'nissan']
color_list = ['red', 'white', 'blue']

data = {'cars': car_list, 'colors': color_list}

# Creating the DataFrame
df = pd.DataFrame(data)

#print(df)

df1 = pd.read_csv(f"data/tickers/symbols_sp500.csv" )

print(df1)
