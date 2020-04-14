# import Libraries
from selenium import webdriver
import pandas as pd


class StockData:

    def clean_data(self, browser):
        df = pd.DataFrame(
            columns=['Symbol', 'Name', 'Price', 'Change', '% Change'])
        data = {}
        index = 1
        while index < 26:
            data['Symbol'] = browser.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[1]/a'.format(index))[0].text
            data['Name'] = browser.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[2]'.format(index))[0].text
            data['Price'] = float(browser.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[3]/span'.format(index))[0].text)
            data['Change'] = float(browser.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[4]/span'.format(index))[0].text)
            data['% Change'] = float(browser.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[5]/span'.format(index))[0].text[:-1].replace(',', ''))

            df = df.append(data, ignore_index=True)
            # Increments the index
            df.index += 1
            index += 1
        return df

    def get_top_gainers(self):
        path = r'./chromedriver.exe'
        url = 'http://finance.yahoo.com/gainers'
        # Use Incognito mode when scraping
        option = webdriver.ChromeOptions()
        option.add_argument('—incognito')
        browser = webdriver.Chrome(executable_path=path, options=option)
        browser.get(url)
        stocks = self.clean_data(browser)
        stocks.to_excel('gainers.xlsx')

    def get_top_losers(self):
        path = r'./chromedriver.exe'
        url = 'http://finance.yahoo.com/losers'
        # Use Incognito mode when scraping
        option = webdriver.ChromeOptions()
        option.add_argument('—incognito')
        browser = webdriver.Chrome(executable_path=path, options=option)
        browser.get(url)
        stocks = self.clean_data(browser)
        stocks.to_excel('top_losers.xlsx')

    def get_most_active(self):
        # Get top 25 most active
        # http://finance.yahoo.com/most-active
        path = r'./chromedriver.exe'
        url = 'http://finance.yahoo.com/most-active'
        # Use Incognito mode when scraping
        option = webdriver.ChromeOptions()
        option.add_argument('—incognito')
        browser = webdriver.Chrome(executable_path=path, options=option)
        browser.get(url)
        stocks = self.clean_data(browser)
        stocks.to_excel('most_active.xlsx')


output = StockData()
output.get_top_gainers()
