from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import csv
from bs4 import BeautifulSoup
from numpy import genfromtxt
import time
import re

myFile = open('zaralokacje.csv', 'w', encoding='utf-8')
with myFile:
    writer = csv.writer(myFile)
    writer.writerow(['Tytuł','Cena','Miasto1','Galerie1','Miasto2','Galerie2','Miasto3','Galerie3','Zdjęcie','URL'])

my_data = genfromtxt('zaralista-sukienki.csv', delimiter=',', dtype=str)
lokalizacje = genfromtxt('lokalizacje.csv', delimiter=',', dtype=str)

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser: WebDriver = webdriver.Chrome(executable_path='chromedriver', options=option)

lp = 1
wiersz = 1
maxwiersz = 10
alista = []
blista = []
clista = []

while wiersz <= maxwiersz:

    alista.clear()
    blista.clear()
    clista.clear()

    browser.get("" + str(my_data[wiersz]) + "")
    time.sleep(2)

    print(lp)

    tytul = browser.find_element_by_xpath("//*[@id='product']/div[1]/div/div[2]/header/h1").text
    print('Produkt:' + tytul + '')

    cena = browser.find_element_by_xpath("//*[@id='product']/div[1]/div/div[2]/div[1]/span").text
    replaced = re.sub('PLN', '', cena)
    print('Cena:' + replaced + '')

    zdjecie = browser.find_element_by_xpath("//*[@id='main-images']/div[1]/a/img")
    src = zdjecie.get_attribute('src')
    print(src)

    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='product']/div[1]/div/div[2]/div[3]/ul/li[2]/a").click()
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='product-detail-stock-popup']/div/div[1]/div/span").click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[@id='product']/div[1]/div/div[2]/div[3]/ul/li[2]/a").click()
    time.sleep(1)

    try:
        opcja = 0
        maxopcja = 10
        while opcja <= maxopcja:
            try:
                opcja += 1
                browser.find_element_by_xpath("//*[@id='stock-size-10" + str(opcja) + "']").click()
            except:
                opcja += 1
                browser.find_element_by_xpath("//*[@id='stock-size-10" + str(opcja) + "']").click()
    except:
        browser.find_element_by_xpath("//*[@id='product-detail-stock-popup']/div/div[3]/div/section/div[2]/div/form/button").click()
        try:
            min = 1
            max = 3
            w = 0
            while min <= max:
                time.sleep(2)
                w += 1
                lokacja = browser.find_element_by_xpath("//*[@id='store-locator-location']")
                lokacja.clear()
                lokacja.send_keys("" + str(lokalizacje[w]) + "")
                lokacja.submit()
                time.sleep(1)
                try:
                    html = browser.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    for result in soup.find_all('li', class_='result'):
                        idgal = result.get('data-storeid')
                        if w == 1:
                            slownik = {'9060':'Galeria Echo'}
                            zsa = slownik.get('' + idgal + '', 'dupa')
                            alista.append(zsa)
                        elif w == 2:
                            slownik = {
                                '3373':'Arkadia',
                                '3561':'Mokotów',
                                '3687':'Złote Tarasy',
                                '3077':'Marszałkowska',
                                '1409':'Plac Unii',
                                '9010':'Blue City',
                                '3269':'Wola Park',
                                '9085':'Targówek',
                                '12835':'Promenada'}
                            zsb = slownik.get('' + idgal + '', 'dupa')
                            blista.append(zsb)
                        elif w == 3:
                            slownik = {
                                '6496':'Rynek',
                                '3688':'Galeria Krakowska',
                                '3437':'Galeria Kazimierz',
                                '9065':'Bonarka',
                                '3609':'Serenada'}
                            zsc = slownik.get('' + idgal + '', 'dupa')
                            clista.append(zsc)
                except:
                    print('nie moze idgal')
                    continue
        except:
            lp += 1
            wiersz += 1



    if len(alista) != 0:
        miasto1 = 'Kielce'
    else:
        miasto1 = ''
    if len(blista) != 0:
        miasto2 = 'Warszawa'
    else:
        miasto2 = ''
    if len(clista) != 0:
        miasto3 = 'Kraków'
    else:
        miasto3 = ''

    print(miasto1, *alista)
    print(miasto2, *blista)
    print(miasto3, *clista)

    a = str(alista)
    b = str(blista)
    c = str(clista)

    aa = re.sub('[\'\[\]]', '', a)
    bb = re.sub('[\'\[\]]', '', b)
    cc = re.sub('[\'\[\]]', '', c)

    link = str(my_data[wiersz])
    data = [tytul] + [replaced] + [miasto1] + [aa] + [miasto2] + [bb] + [miasto3] + [cc] + [src] + [link]
    myFile = open('zaralokacje.csv', 'a', encoding='utf-8')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(data)

