import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from parser_spb import pars_mult

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

sp500_tickers = []

for i in range(10):
    url = 'https://finasko.com/sp-500-companies/' + str(i+1)
    driver.get(url)
    tickers = driver.find_elements(By.XPATH, "//div/div[@class='stock-symbol']")
    for ticker in tickers:
        sp500_tickers.append(ticker.text)


for i in set(sp500_tickers):
    if sp500_tickers.count(i) > 1:
        print(f'{i} встречается {sp500_tickers.count(i)}')



df_tickers = pd.DataFrame({'tickers': list(set(sp500_tickers))})

for i in range(len(df_tickers)):

    ticker = df_tickers.loc[i].tickers
    url = 'https://finviz.com/quote.ashx?t=' + ticker + '&ty=c&ta=1&p=d'
    driver.get(url)

    try:
        name_company = driver.find_element(By.XPATH, "//tr/td/h1/span/a[@class='tab-link']").text

    except:
        df_tickers = df_tickers.drop(i)


df_tickers = df_tickers.reset_index(drop=True)



df_finviz = pd.DataFrame()

df_finviz = pars_mult(df_tickers, df_finviz)

df_finviz = df_finviz.drop(['Dividend', 'Market Cap', 'Employees', 'Optionable', 'Shortable', 'Earnings'], axis=1)


file_name = 'sp500.csv'

df_finviz.to_csv(file_name, encoding='utf-8', index=False)

driver.quit()