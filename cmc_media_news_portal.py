from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import urllib.request
import csv
from bs4 import BeautifulSoup
import time
import os
import re
from PIL import Image

option = webdriver.ChromeOptions()
option.add_argument("--incognito")
#option.add_argument("--headless")
browser: WebDriver = webdriver.Chrome(executable_path='chromedriver', options=option)

myFile = open('lista.csv', 'w', encoding='utf-8', newline='')

for x in range(1, 50):
    browser.get("https://nowagazeta.pl/wiadomosci/strona%s" % x)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')


    for link in soup.find_all('li', class_='c-news-list-item'):
        try:

            url = link.find('a')['href']
            url_string = "https://nowagazeta.pl"+url

            print(url)

            browser.get(url_string)
            time.sleep(5)

            html2 = browser.page_source
            soup2 = BeautifulSoup(html2, 'html.parser')

            tytul = soup2.find('h1', class_="l-news__title").text
            print(tytul)
            zdjecie = soup2.find('img', class_="l-news__image").attrs['src']
            tekst = soup2.find('div', class_="c-content").text
            autor = soup2.find('span', class_="author").text
            data = soup2.find('span', class_="c-news__date").text

            line = [tytul] + [zdjecie] + [re.sub('\s*\n\s*', '<br>', tekst] + [autor] + [data]

            myFile = open('lista.csv', 'a', encoding='utf-8', newline='')
            with myFile:
                writer = csv.writer(myFile, delimiter =';')
                writer.writerow(line)

        except: continue
