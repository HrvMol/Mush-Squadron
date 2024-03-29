from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
service = webdriver.FirefoxService(executable_path='/home/pi/.cargo/bin/geckodriver')
driver = webdriver.Firefox(options=options, service=service)

driver.get('https://google.com')

soup = BeautifulSoup(driver.page_source, 'html.parser')

print(soup)