import time
from selenium import webdriver
from raspagem_categoria import rasparCategoria
import time
import sqlite3
import os.path

## Setup
# Conexão
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "conexao.db")

connector = sqlite3.connect(db_path)
cursor = connector.cursor()
while True:
    antes = time.time()
    # Selenium
    driver = webdriver.Chrome()

    # Obter os links das categorias 
    cursor.execute('''
        SELECT catLink FROM Category;
    ''')

    for link in cursor.fetchall():
        rasparCategoria(connector, cursor, driver, link[0]) #link[0] pois link retorna tupla
        
    driver.close()

    agora = time.time()
    delta = agora - antes
    if (delta < 3600):
        time.sleep(3600 - delta)


""" TESTES
# Selenium
driver = webdriver.Chrome()

rasparCategoria(connector, cursor, driver, 'https://www.amazon.com.br/gp/bestsellers/books/') # TESTES

driver.close()
"""