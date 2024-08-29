from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cerca_oggetto(name : str):
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.it/")

    element = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.NAME,"field-keywords"))
    ) 

    element.send_keys(name)
    element.submit()
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    prodotti = soup.find_all("div", {"data-component-type" : "s-search-result"})
    
    risultato = ""
    trovati = 0
    for prodotto in prodotti:
        title = prodotto.h2.text.strip()
        
        #unisce url di amazon con url del prodotto
        url = "https://www.amazon.it" + prodotto.h2.a['href']

        # estrazione del prezzo
        price_whole = prodotto.find("span", {"class": "a-price-whole"}) #parte intera
        price_fraction = prodotto.find("span", {"class": "a-price-fraction"}) # parte frazionaria 
        
        # unisce il prezzo e cerca il prezzo giusto
        if price_whole and price_fraction:
            price = price_whole.text + price_fraction.text
            risultato += f"{trovati})Titolo: {title}\nPrezzo: {price}\nUrl: {url}\n\n"
            trovati += 1
        
            
    with open("botVocale/risultato/risultato.txt", mode="w", encoding= "utf-8") as f:
        f.write(risultato)
        
    driver.quit()
    return trovati

