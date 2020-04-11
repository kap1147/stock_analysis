# import Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time


def getdata():
    path = r'./chromedriver.exe'
    url = 'http://finance.yahoo.com/most-active'
    # Use Incognito mode when scraping
    option = webdriver.ChromeOptions()
    option.add_argument('—incognito')
    browser = webdriver.Chrome(executable_path=path, options=option)
    browser.get(url)

    df = pd.DataFrame(columns=['Name', 'Price', 'Change', '% Change',
                               'Volume', 'Avg Volume (3 months)', 'Market Cap'])
    data = {}
    index = 1
    while index < 26:
        data['Name'] = browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[2]'.format(index))[0].text
        data['Price'] = float(browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[3]/span'.format(index))[0].text)
        data['Change'] = browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[4]/span'.format(index))[0].text
        data['% Change'] = browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[5]/span'.format(index))[0].text
        data['Volume'] = browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[6]/span'.format(index))[0].text
        data['Avg Volume (3 months)'] = browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[7]'.format(index))[0].text
        data['Market Cap'] = browser.find_elements_by_xpath(
            '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[8]/span'.format(index))[0].text

        df = df.append(data, ignore_index=True)
        # Increments the index
        df.index += 1
        index += 1
    return df


output = getdata()
print(output)
output.to_excel('test.xlsx')
