from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.formatar_data import formatar_data 
import datetime

def rasparCategoria(connector, cursor, driver, link):
    driver.get(link) 

    # Esperar cada elemento carregar
    bookContainerList = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.a-section.a-spacing-none.aok-relative'))
    )
    proName = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p13n-sc-truncated')))
    
    bookContainerList = bookContainerList[:10] # Pegar somente os 10 primeiros elementos

    # init
    data = []
    catExists = False

    # Percorre cada cointaner de livro
    for element in bookContainerList:
        
        ### Scrapping Pagina principal
        # titulo
        proName = element.find_element_by_css_selector('div.p13n-sc-truncated')

        if proName:
            if proName.get_attribute("title") == "":
                proName = proName.text
            else:
                proName = proName.get_attribute("title")
                
        proName = proName if proName else "N/A"

        # Procura se já existe registro do livro dado o nome
        cursor.execute("""SELECT proCode FROM Product WHERE proName = (?)""", (proName,)) 
        proCode = cursor.fetchone()

        if not proCode: # Se for o primeiro registro...
            # link do livro
            livroLinkPai = element.find_elements_by_css_selector("span.aok-inline-block.zg-item") # pega o pai
            proLink = livroLinkPai[0].find_element_by_xpath(".//*").get_attribute("href") # pega o filho
        else:
            proLink = "N/A"

        # raspa categoria do livro
        try:
            proCategory = element.find_elements_by_xpath('//*[@id="zg_browseRoot"]/ul/li/span')[0].text # categoria unica
        except:
            try:
                proCategory = element.find_elements_by_xpath('//*[@id="zg_browseRoot"]/ul/ul/li/span')[0].text 
            except:
                proCategory = element.find_elements_by_xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li/span')[0].text 
            
        proCategory = proCategory if len(proCategory) != 0 else "N/A"

        # posicao
        proPosition = element.find_element_by_css_selector('span.zg-badge-text').text
        proPosition = int(proPosition.replace("#", ""))
        proPosition = proPosition if proPosition else "N/A"

        # autor
        try:
            authorParent = element.find_element_by_css_selector("div.a-row.a-size-small")
            autName = authorParent.find_element_by_xpath('.//*')
            autName = autName.text if autName else "N/A"
        except:
            autName = "not exists" # A Amazon não inseriu author

        # qtd review
        proReview = element.find_elements_by_css_selector('a.a-size-small.a-link-normal') 
        proReview = int((proReview[0].text).replace(".", "")) if len(proReview) != 0 else "N/A"

        # qtd estrelas
        stars = element.find_elements_by_css_selector('i.a-icon.a-icon-star') 
        if len(stars) != 0:
            proStar = stars[0].find_element_by_xpath('..')
            proStar = float(((proStar.get_attribute("title")).split()[0]).replace(",", ".")) if proStar else "N/A"
        else: 
            proStar = "N/A"

        # tipo livro
        try:
            proType = element.find_element_by_css_selector('span.a-size-small.a-color-secondary')
            proType = proType.text if proType else "N/A"
        except:
            proType = "Not Exists"

        # preco
        try:
            proPrice = element.find_element_by_css_selector('span.p13n-sc-price').text
            proPrice = float((proPrice.split(" ")[1]).replace(",", "."))
        except:
            proPrice = -1

        # link da imagem
        proImage = element.find_elements_by_css_selector("div.a-section.a-spacing-small")
        proImage = proImage[0].find_element_by_xpath(".//*").get_attribute("src")
        proImage = proImage if proImage else "N/A"


        
                 
        ### Salvar os dados numa lista 
        data.append({
            'title': proName,
            'position': proPosition,
            'author': autName,
            'stars': proStar,
            'review': proReview,
            'typeBook': proType,
            'price': proPrice,
            'link': proLink,
            'img': proImage,
            'category': proCategory,
            'scrapDate': (datetime.datetime.now()).strftime("%d/%m/%y %H:%M:%S")
        }) 
    
    for book in data:
        # init
        spanHeaderList = []
        spanTextList = []
        pages = None
        publisher = None
        publishDate = None
        language = None

        book['publisher'] = "N/A"
        book['publishDate'] = "N/A"
        book['language'] = "N/A"
        book['pages'] = "N/A"
 
        if book["link"] != "N/A":
            driver.get(book["link"]) # entra no link do livro especifico
            
            try:
                bookDetailsList = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.ID, 'detailBullets_feature_div'))
                )

                bookDetails = bookDetailsList[1]
                bookDetailsElements = bookDetails.find_elements_by_tag_name('li')
                
                for li in bookDetailsElements:
                    spanHeaderList.append(li.find_elements_by_tag_name('span')[1].text) 
                    spanTextList.append(li.find_elements_by_tag_name('span')[2].text)
                    
                spanHeaderList = list(map(lambda li: li.replace(" :", ""), spanHeaderList))

                for j in range(len(spanHeaderList)):
                    if spanHeaderList[j] == "Editora": 
                        inicio = spanTextList[j]
                        publishDate = inicio.split("(")[-1]
                        publisher = inicio.split("(")[0]
                        if ";" in publisher:
                            publisher = publisher.split(";")[0]
                        publishDate = publishDate.replace(")", "")
                    elif spanHeaderList[j] == "Idioma":
                        language = spanTextList[j]
                    elif spanHeaderList[j] == book["typeBook"] or spanHeaderList[j] == "Número de páginas":
                        pages = int(spanTextList[j].split()[0])
            except:
                continue

        # Pega o ultimo dado acoplado e adiciona info
        if publisher:
            book['publisher'] = publisher

        if publishDate:
            book['publishDate'] = formatar_data(publishDate)

        if language:
            book['language'] = language

        if pages:
            book['pages'] = pages
 
 
   # Salvar no banco
    for book in data:
        # Product
        cursor.execute("""SELECT autCode FROM Author WHERE autName = (?)""", (book["author"],)) 

        autCode = cursor.fetchone()

        if autCode:
            autCode = autCode[0]
            # retornar codigo existente
            if(book["link"] == "N/A"): # Autor existe e é o mesmo livro
                cursor.execute('''INSERT INTO Product (autCode, proName, proType, proPrice, proPosition, proStar, proReview, proImage, proScrapDate) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',  
                        (autCode, book["title"], book["typeBook"], book["price"], book["position"], book["stars"], book["review"], book["img"], book["scrapDate"]))
                connector.commit()
                proCode = cursor.lastrowid # pega o id da linha criada acima
            else: # autor existe mas não é o mesmo livro
                cursor.execute('''INSERT INTO Product (autCode, proName, proType, proPrice, proPosition, proStar, proReview, proLink, proImage, proLanguage, proPages, proPublishedDate, proPublisher, proScrapDate) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',  
                        (autCode, book["title"], book["typeBook"], book["price"], book["position"], book["stars"], book["review"], book["link"], book["img"], book["language"], book["pages"], book["publishDate"], book["publisher"], book["scrapDate"]))
                connector.commit()
                proCode = cursor.lastrowid # pega o id da linha criada acima
        else:
            cursor.execute('INSERT INTO Author (autName) VALUES (?)', (book["author"],))
            connector.commit()
            autCode = cursor.lastrowid # pega o id da linha criada acima
            cursor.execute('''INSERT INTO Product (autCode, proName, proType, proPrice, proPosition, proStar, proReview, proLink, proImage, proLanguage, proPages, proPublishedDate, proPublisher, proScrapDate) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',  
                    (autCode, book["title"], book["typeBook"], book["price"], book["position"], book["stars"], book["review"], book["link"], book["img"], book["language"], book["pages"], book["publishDate"], book["publisher"], book["scrapDate"]))
            connector.commit()
            proCode = cursor.lastrowid # pega o id da linha criada acima

        # Verificar existencia de registro desse livro dessa categoria no banco:
        cursor.execute('''SELECT catName 
            FROM Category c
            INNER JOIN Product_Category pc
            ON c.catCode = pc.catCode
            INNER JOIN Product p
            ON p.proCode = pc.proCode
            WHERE pc.proCode = (?);''', (proCode,))

        for cat in cursor.fetchall():
            catExists = True if proCategory == cat[0].replace(",", "") else False

        if not catExists:
            cursor.execute("SELECT catCode FROM Category WHERE catName = (?)", (proCategory, ))
            cursor.execute("INSERT INTO Product_Category (proCode, catCode) VALUES (?, ?)", (proCode, cursor.fetchone()[0]))
            connector.commit()


