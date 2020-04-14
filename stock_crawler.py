# import Libraries
from selenium import webdriver
import pandas as pd


class YFStockData:
    def get_data(self, url):
        # Configure and make request with Selenium
        path = r'./chromedriver.exe'
        option = webdriver.ChromeOptions()
        option.add_argument('—incognito')
        browser = webdriver.Chrome(executable_path=path, options=option)
        browser.get(url)
        return browser

    def clean_data(self, data):
        dataframe = pd.DataFrame(
            columns=['Symbol', 'Name', 'Price', 'Change', '% Change'])
        data_arr = {}
        index = 1
        while index < 26:
            data_arr['Symbol'] = data.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[1]/a'.format(index))[0].text
            data_arr['Name'] = data.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[2]'.format(index))[0].text
            data_arr['Price'] = float(data.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[3]/span'.format(index))[0].text)
            data_arr['Change'] = float(data.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[4]/span'.format(index))[0].text)
            data_arr['% Change'] = float(data.find_elements_by_xpath(
                '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[5]/span'.format(index))[0].text[:-1].replace(',', ''))

            dataframe = dataframe.append(data_arr, ignore_index=True)
            dataframe.index += 1
            index += 1
        return dataframe

    def get_top_gainers(self):
        # Get top 25 best gainers
        url = 'http://finance.yahoo.com/gainers'
        data = self.get_data(url)
        stocks = self.clean_data(data)
        stocks.to_excel('gainers.xlsx')

    def get_top_losers(self):
        # Get top 25 worst performers
        url = 'http://finance.yahoo.com/losers'
        data = self.get_data(url)
        stocks = self.clean_data(data)
        stocks.to_excel('top_losers.xlsx')

    def get_most_active(self):
        # Get top 25 most active
        url = 'http://finance.yahoo.com/most-active'
        data = self.get_data(url)
        stocks = self.clean_data(data)
        stocks.to_excel('most_active.xlsx')


stocks = YFStockData()
stocks.get_top_losers()
