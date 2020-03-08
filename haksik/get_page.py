from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

options = Options()
options.headless = True

url = 'http://www.duksung.ac.kr/diet/schedule.do?menuId=1151'
driver = webdriver.Firefox(options=options)
driver.get(url)
driver.implicitly_wait(5)
sleep(3)

html = driver.page_source
out_fp = open('page.html', 'w', encoding='utf-8')
out_fp.write(html)

out_fp.close()
driver.close()
