def formatar_data(data_inicio):    
    data_inicio = data_inicio.split(" ")
    mes = data_inicio[1].lower()
    if mes == "janeiro":
        mes = "01"
    elif mes == "fevereiro":
        mes = "02"
    elif mes == "março":
        mes = "03"
    elif mes == "abril":
        mes = "04"
    elif mes == "maio":
        mes = "05"
    elif mes == "junho":
        mes = "06"
    elif mes == "julho":
        mes = "07"
    elif mes == "agosto":
        mes = "08"
    elif mes == "setembro":
        mes = "09"
    elif mes == "outubro":
        mes = "10"
    elif mes == "novembro":
        mes = "11"
    elif mes == "dezembro":
        mes = "12"
    else: 
        mes = "erro"

    return f"{data_inicio[0]}/{mes}/{data_inicio[2]}"
