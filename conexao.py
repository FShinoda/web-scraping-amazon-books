# AMAZON BOOKS DATA ANALYSING
import sqlite3
connector = sqlite3.connect('conexao.db')
cursor = connector.cursor()

# Drop
"""
cursor.execute(''' DROP TABLE IF EXISTS Product; ''')
cursor.execute(''' DROP TABLE IF EXISTS Author; ''')
cursor.execute(''' DROP TABLE IF EXISTS Category; ''')
"""

# Creating Tables

# Author
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Author (
        autCode INTEGER PRIMARY KEY AUTOINCREMENT,
        autName VARCHAR(200) NOT NULL
    );
''')
connector.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
        catCode INTEGER PRIMARY KEY NOT NULL,
        catName VARCHAR(200) NOT NULL,
        catLink TEXT NOT NULL
    )
''')
connector.commit()

# Product
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        proCode INTEGER PRIMARY KEY AUTOINCREMENT,
        autCode INTEGER NOT NULL,
        proName VARCHAR(60) NOT NULL,
        proType VARCHAR(45) NULL,
        proPrice DECIMAL(7, 2) NOT NULL,
        proPosition INTEGER NOT NULL,
        proStar DECIMAL(1,1) NULL,
        proReview INTEGER NULL,
        proLanguage VARCHAR(45) NULL,
        proPages INTEGER NULL,
        proPublishedDate Date NULL,
        proScrapDate Datetime NOT NULL,
        proLink TEXT NULL,
        proPublisher VARCHAR(45) NULL,
        proImage TEXT NULL,
        FOREIGN KEY (autCode) REFERENCES Author(autCode)
    );
''')
connector.commit()

cursor.execute('''
    CREATE INDEX idx_proName
    ON Product(proName);
''')
connector.commit()

# Tabela de chave composta
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product_Category (
        pro_catCode INTEGER PRIMARY KEY AUTOINCREMENT,
        proCode INTEGER,
        catCode INTEGER,
        FOREIGN KEY (proCode) REFERENCES Product(proCode),
        FOREIGN KEY (catCode) REFERENCES Category(catCode)
    )
''')
connector.commit()

# Static Insert
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (01, "Livros", "https://www.amazon.com.br/gp/bestsellers/books/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (02, "Autoajuda", "https://www.amazon.com.br/gp/bestsellers/books/7841720011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (03, "Ficção Científica", "https://www.amazon.com.br/gp/bestsellers/books/7841776011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (04, "HQs, Mangás e Graphic Novels", "https://www.amazon.com.br/gp/bestsellers/books/7842710011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (05, "Direito", "https://www.amazon.com.br/gp/bestsellers/books/7874340011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (06, "Administração, Negócios e Economia", "https://www.amazon.com.br/gp/bestsellers/books/7872854011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (07, "Arte, Cinema e Fotografia", "https://www.amazon.com.br/gp/bestsellers/books/7841296011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (08, "Artesanato, Casa e Estilo de Vida", "https://www.amazon.com.br/gp/bestsellers/books/7841521011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (09, "Biografias e Histórias Reais", "https://www.amazon.com.br/gp/bestsellers/books/7841731011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (10, "Educação, Referência e Didáticos", "https://www.amazon.com.br/gp/bestsellers/books/7842837011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (11, "Esportes e Lazer", "https://www.amazon.com.br/gp/bestsellers/books/7842741011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (12, "Gastronomia e Culinária", "https://www.amazon.com.br/gp/bestsellers/books/7872552011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (13, "Infantil", "https://www.amazon.com.br/gp/bestsellers/books/7844001011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (14, "Policial, Suspense e Mistério", "https://www.amazon.com.br/gp/bestsellers/books/7872829011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (15, "Política, Filosofia e Ciências Sociais", "https://www.amazon.com.br/gp/bestsellers/books/7873971011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (16, "Religião e Espiritualidade", "https://www.amazon.com.br/gp/bestsellers/books/7874675011/");
''')
connector.commit()
cursor.execute('''
    INSERT INTO Category (catCode, catName, catLink)
        VALUES (17, "Turismo e Guias de Viagem", "https://www.amazon.com.br/gp/bestsellers/books/7882554011/");
''')
connector.commit()



if __name__ == '__main__':
    
    print('Tables added.')

connector.close()
