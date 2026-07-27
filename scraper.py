from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

# options = Options()
# options.add_argument("--start-maximized")
driver = webdriver.Chrome()#options=options)

driver.get("https://grid-india.in/en/reports/daily-psp-report")
wait = WebDriverWait(driver, 20)

table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/main/div/div[3]/div/div/div[2]/table')))
table_html = table.get_attribute("outerHTML")

soup = BeautifulSoup(table_html, 'html.parser')
table = soup.find('table')
all_data = []
for tr in table.find('tbody').find_all('tr'):
    row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
    download_view_td = tr.find_all('td')[-1]
    href = download_view_td.find('a', href=True)['href'] if download_view_td.find('a', href=True) else None
    row_data.append(href)
    all_data.append(row_data)
headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
headers.append('URL')
df = pd.DataFrame(all_data, columns=headers)
driver.quit()

print(df)
