from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import csv
from bs4 import BeautifulSoup
import re

plik = csv.writer(open('mm-telewizory-bronowice.csv', 'w'))
plik.writerow(['ID','Nazwa', 'Cena', 'Url', 'Obrazek', 'Miasto', 'Galeria', 'Sklep', 'Kategoria', 'Podkategoria'])

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
#option.add_argument("--headless")

# Create new Instance of Chrome in incognito mode
browser: WebDriver = webdriver.Chrome(executable_path='chromedriver', options=option)

# Go to desired website
browser.get("https://mediamarkt.pl/rtv-i-telewizory/telewizory?sort=0&limit=100&page=1")

browser.find_element_by_xpath("//*[@id='js-product-listing']/div[1]/div/div/div[2]/form/div/label/div/div[2]/p").click() #klika żeby wyswietlilo 100 produktow
browser.find_element_by_xpath("//*[@id='js-product-listing']/div[1]/div/div/div[2]/form/div/label/div/div[3]/div/ul/li[28]").click() #klika w Galerię Bronowice Kraków

zrodlo = browser.page_source
przekaz = BeautifulSoup(zrodlo, 'html.parser')
ilosc = przekaz.find('span', class_='m-pagination_count')
ilosctostr = str(ilosc)
wyczytaj = re.findall('[0-9]+', ilosctostr)
wyczytajtostr = str(wyczytaj)
usun = re.sub('\W+', '', wyczytajtostr)
zamiennaint = int(usun)
print(zamiennaint)

def pajak(max_pages):
        lp = 0
        page = 1
        while page <= max_pages:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                for paczka in soup.find_all('div', class_='m-productsBox_containerInner'):

                        lp += 1
                        print(lp)

                        tytul = paczka.find('a')['title']
                        print(tytul)

                        cena = paczka.find('div', itemprop='price')
                        cenastr = str(cena)
                        znajdz = re.findall('[0-9]+', cenastr)
                        znajdzstr = str(znajdz)
                        replaced = re.sub('\W+', '', znajdzstr)
                        print(replaced)

                        adres = paczka.find('a')['href']
                        padres = 'https://mediamarkt.pl' + adres
                        print(padres)

                        obraz = paczka.find('img')['data-target']
                        pobraz = 'http:' + obraz
                        print(pobraz)

                        plik.writerow([lp, tytul, replaced, padres, pobraz,'Kraków','ul. Radomska','Media Markt','Elektronika','Telewizory'])
                page += 1
                if page > zamiennaint: break
                browser.find_element_by_class_name('m-pagination_next').click()
pajak(zamiennaint)
