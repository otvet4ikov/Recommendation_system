import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def data_to_series(data):
    lst = []
    for element in data:
        lst.append(element.text)
    series = pd.Series(lst)
    return series



def pars_mult(df_start, df_end):

    """
    Функция для парсинга данных по тикерам с finviz
    :param df_start:  датафрейм данных, который содержит тикеры компании
    :param df_end:  датафрейм с конечными данными
    :return: датафрейм с данными
    """

    for i in range(len(df_start)):
        df = pd.DataFrame()
        ticker = df_start.loc[i].tickers
        url = 'https://finviz.com/quote.ashx?t=' + ticker + '&ty=c&ta=1&p=d'

        driver.get(url)

        industry = driver.find_element(By.XPATH, "//tr/td/a[@class='tab-link']").text
        multipliers = driver.find_elements(By.XPATH, "//div/table/tbody/tr/td[@class='snapshot-td2-cp']")
        content = driver.find_elements(By.XPATH, "//div/table/tbody/tr/td[@class='snapshot-td2']")[0:72]

        df['Ticker'] = [ticker]
        df['Industry'] = [industry]
        for j in range(len(content)):
            df[multipliers[j].text] = content[j].text

        df_end = pd.concat([df_end, df])

    return df_end

#парсим тикеры, название компании списка СПБ100

url = 'https://spbexchange.ru/ru/stocks/index/SPB100/'
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.get(url)


content = driver.find_element(By.XPATH, "//ul/li[@data-tab='tab-2']")
content.click()


tickers = driver.find_elements(By.XPATH, "//tr/td[2]")
company_names = driver.find_elements(By.XPATH, "//tr/td[3]")


tickers_spb = data_to_series(tickers)
companies_spb = data_to_series(company_names)


df_spb = pd.DataFrame({'tickers': tickers_spb,
                 'name_company': companies_spb})

#проверяем, есть ли все тикеры на finviz

for i in range(len(df_spb)):

    ticker = df_spb.loc[i].tickers
    url = 'https://finviz.com/quote.ashx?t=' + ticker + '&ty=c&ta=1&p=d'
    driver.get(url)

    try:
        name_company = driver.find_element(By.XPATH, "//tr/td/h1/span/a[@class='tab-link']").text
        print(str(i)+')', df_spb.loc[i].name_company, '|',name_company)

    except:
        print('Error', df_spb.loc[i].name_company)
        df_spb = df_spb.drop(i)


#дропаем первый индекс, так как там не та компания и обновляем индексы у датафрейма
df_spb = df_spb.drop(1)
df_spb = df_spb.reset_index(drop=True)

df_finviz = pd.DataFrame()

df_finviz = pars_mult(df_spb, df_finviz)

df_finviz df_finviz.drop(['Dividend', 'Market Cap', 'Employees', 'Optionable', 'Shortable', 'Earnings'], axis=1)


file_name = 'spb100.csv'

df_finviz.to_csv(file_name, encoding='utf-8', index=False)

driver.quit()