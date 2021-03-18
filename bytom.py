from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import csv
from bs4 import BeautifulSoup
from numpy import genfromtxt
import numpy

plik = csv.writer(open('rozmiarygalerie.csv', 'w'))
plik.writerow(['Tytul','Miasto','Galeria'])

my_data = genfromtxt('file.csv', delimiter=',', dtype=str)

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser: WebDriver = webdriver.Chrome(executable_path='chromedriver', options=option)

lp = 1
wiersz = 1
maxwiersz = 2

while wiersz <= maxwiersz:

    browser.get("" + str(my_data[wiersz]) + "")
    time.sleep(1)
    tytul = browser.find_element_by_xpath("/html/body/byt-root/byt-base-layout/div/byt-product/section/div/byt-product-cart-box/div/div[2]/span[1]").text
    print('Produkt:' + tytul + '')
    opcja = 2
    maxopcja = 25

    while opcja <= maxopcja:

        try:
            browser.find_element_by_xpath("//*[@id='attribute_413']/option[" + str(opcja) + "]").click()
        except:
            print('Koniec listy rozmiarów, przechodzę do następnego produktu ...\n\n')
            opcja = 2
            wiersz += 1
            browser.get("" + str(my_data[wiersz]) + "")
            tytul = browser.find_element_by_xpath("//*[@id='product-description']/h2").text
            time.sleep(1)
            print('Produkt:' + tytul + '')

        rozmiar = browser.find_element_by_xpath("//*[@id='attribute_413']/option[" + str(opcja) + "]").text
        print('\nRozmiar:' + rozmiar + '\n')
        time.sleep(2)
        klik = browser.find_element_by_xpath("//*[@id='product-description']/div[4]/div/ul/li[2]/a")
        browser.execute_script("arguments[0].click();", klik)
        time.sleep(2)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for paczka in soup.find_all('div', class_='col-md-4 col-sm-6'):

            mig = paczka.find('strong').text
            miasto, galeria = mig.split('/')
            print('' + miasto + ', ' + galeria + '')
            plik.writerow([tytul, miasto, galeria])

        opcja += 1

    wiersz += 1
    lp += 1


