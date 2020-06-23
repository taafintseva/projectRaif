from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import requests

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        ads = soup.find_all('span',
                            class_='item__location__address__link pseudo-link')
    except AttributeError:
        print("AAAAA")
    for ad in ads:
        write_csv(ad)


def write_csv(ad):
    with open('bankraif.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(ad)


def main():
    base_url = 'https://www.banki.ru/banks/map/moskva/#/!b1:4389!s3:all!s4:list!m1:10!m2:55.755773!m3:37.617761!p1:1'
    browser = webdriver.Firefox()
    browser.get(base_url)

    for i in range(1, 15):
        if not(i - 1):
            time.sleep(30)
        else:
            time.sleep(0.5)
        html = browser.page_source
        get_page_data(html)
        a = browser.find_element_by_xpath("//a[@class='icon-font icon-arrow-next-16 icon-font--size_small']")
        a.click()
    browser.quit()


if __name__=='__main__':
    main()
