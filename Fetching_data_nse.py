from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cservice = webdriver.ChromeService(executable_path='D:/Prasad/testing/chromedriver.exe')     #instead of static chromedriver file we can use chromedrive manager as well to auto download chromedriver based on current version of chrome installed.
driver = webdriver.Chrome(service=cservice)
driver.maximize_window()
header_list = []
company_data_list = []
try:
    driver.get('https://www.nseindia.com/market-data/live-equity-market')
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="market-Equity-Stock"]'))).click()
    time.sleep(5)
    select =  Select(driver.find_element(By.XPATH,'//*[@id="equitieStockSelect"]'))
    select.select_by_visible_text('NIFTY 50')
    ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equityStockTable"]')))

    
    rows = ele.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'th')  
        cells1 = row.find_elements(By.TAG_NAME, 'td')  
        row_data = [cell.text.strip() for cell in cells]
        row_data1 = [cell.text.strip() for cell in cells1]
        header_list.append(row_data)
        company_data_list.append(row_data1)
except Exception as e:
    print(e)    
header_df = pd.DataFrame(header_list)
(header_df.dropna(inplace=True))
company_data_df = pd.DataFrame(company_data_list)
company_data_df.dropna(inplace=True)
concatenated_df = pd.concat([header_df, company_data_df])
final_val = concatenated_df.head(16)  #it will provide 15 records except column header.
final_val.to_excel('D:/Prasad/testing/output.xlsx', index=False)     #change path of excel file
print('output file successfully generated')