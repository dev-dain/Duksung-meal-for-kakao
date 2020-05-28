# Import
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import os
import sys

# Function
def get_options():
    options = Options()
    options.headless = True
    return options

def get_html(driver, url):
    driver.get(url)
    driver.implicitly_wait(5)
    sleep(3) #sleep이 있어야 dateTime class, dietNoteContent id 콘텐츠를 볼 수 있음

    html = driver.page_source
    return html

def find_table(html):
    soup = BeautifulSoup(html, 'lxml')
    target_table = soup.find(id='schedule-table')
    return target_table

def get_info(target_table):
    info_str = target_table.find_all("th")
    for i in range(len(info_str)):
        info_str[i] = info_str[i].get_text('\n')+'\r\r'
    return info_str

def get_meal(target_table):
    meal_str = target_table.find_all("td")
    for i in range(len(meal_str)):
        meal_str[i] = meal_str[i].get_text('\n')+'\r\r'
    return meal_str

def go_crawl():
    if os.path.exists('week_meal.txt'):
        os.remove('week_meal.txt')
    if os.path.exists('week_info.txt'):
        os.remove('week_info.txt')

    url = 'http://www.duksung.ac.kr/diet/schedule.do?menuId=1151'
    options = get_options()
    driver = webdriver.Firefox(options=options, executable_path=r'/home/ubuntu/geckodriver')

    try:
        html = get_html(driver, url)
    except:
        sys.exit()

    target_table = find_table(html)
    info_str = get_info(target_table)
    meal_str = get_meal(target_table)

    meal_fp = open('/home/ubuntu/haksik_project/haksik/week_meal.txt', 'w', encoding='utf-8')
    meal_fp.writelines(meal_str)
    meal_fp.close()
    info_fp = open('/home/ubuntu/haksik_project/haksik/week_info.txt', 'w', encoding='utf-8')
    info_fp.writelines(info_str)
    info_fp.close()

    driver.close()


# Main
if __name__ == '__main__':
    go_crawl()
