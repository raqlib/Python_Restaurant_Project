import json
import re
import datetime
from datetime import date
import time

#Função escrita/criação do ficheiro json
def guardarDados(lista, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(lista, f, indent=4)
    except:
        print("\Erro: não foi possível gravar o ficheiro!")
    else:
        print("\nFicheiro guardado!")


#Função para ler ficheiros json
def lerFicheirosJson(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)  
        if isinstance(data, dict):
            return [data]
        if isinstance(data[0],dict):
            return data
    except:
        print("\nErro: não foi possivel abrir o ficheiro!\n")

#Função para criar dicionário das propriedades do restaurante
def criarDefinitions():
    definitions = {
        "preco_adulto": 25,
        "preco_crianca": 15,
        "dia_folga": "Monday",
        "abertura" : "19:00",
        "fecho" : "22:00",
        "ocupacao_maxima": 100,
        "num_mesas_disponiveis": 20
    }

    guardarDados(definitions, "definitions.json")      

    return definitions

#Função para criar lista de dicionários de users
def criarUsers():
    users = []
    users.append({"email": "gervasio@hotmail.com", "permission": "client"})
    users.append({"email": "anacleto@hotmail.com","permission": "client"})
    users.append({"email": "joaquim@hotmail.com","permission": "client"})
    users.append({"email": "celeste@hotmail.com","permission": "client"})
    users.append({"email": "angelica@hotmail.com","permission": "client"})
    users.append({"email": "rosario@hotmail.com","permission": "client"})
    users.append({"email": "madalena@hotmail.com","permission": "client"})
    users.append({"email": "olinda@hotmail.com","permission": "client"})
    users.append({"email": "gertrudes@hotmail.com","permission": "client"})
    users.append({"email": "cesaltina@hotmail.com","password": "123","permission": "admin"})
    users.append({"email": "encarnacao@hotmail.com","password": "321","permission": "admin"})
    users.append({"email": "luisa@hotmail.com","password": "396","permission": "admin"})
    users.append({"email": "maria@hotmail.com","permission": "client"})
    users.append({"email": "maria2@hotmail.com","permission": "client"})
    users.append({"email": "maria3@hotmail.com","permission": "client"})
    users.append({"email": "rodolfo@hotmail.com","permission": "client"})

    guardarDados(users,"users.json")

    return users

#Função para criar lista de dicionários de dias de fecho do restaurante
def criarCloseDays():
    closedays = []
    closedays.append({"dia_fecho":"2023-11-30"})
    closedays.append({"dia_fecho":"2023-12-25"})
    closedays.append({"dia_fecho":"2024-01-09"})
    closedays.append({"dia_fecho":"2024-02-22"})
    closedays.append({"dia_fecho":"2024-03-20"})
    closedays.append({"dia_fecho":"2024-04-15"})
    closedays.append({"dia_fecho":"2024-05-05"})
    closedays.append({"dia_fecho":"2024-06-17"})
    closedays.append({"dia_fecho":"2024-08-09"})
    closedays.append({"dia_fecho":"2024-09-05"})
    closedays.append({"dia_fecho":"2024-10-15"})

    guardarDados(closedays,"closedays.json")

    return closedays


#Função para criar lista de dicionários de refeições dos clientes
def criarMeals(email, data, hora, adultos, criancas, nomeCliente, nif, total):

    confirm = False

    try:
        with open("meals.json", 'r') as f:
            meals = json.load(f)
    except:
        print("Erro")
        meals = []

    temp = {
        "email":email,
        "data":data,
        "hora":hora,
        "numero_adultos": adultos,
        "numero_criancas":criancas,
        "nome_cliente":nomeCliente,
        "nif":nif,
        "total_pagar":total
    }
    
    reserva = reservaRepetida(data,meals, email)

    if not reserva:
        #imprimir dados da reserva
        print("\nResumo da reserva: ")
        print(f"Data: {temp['data']} \t Hora: {temp['hora']}")
        print(f"Número de adultos: {temp['numero_adultos']} \t Número de crianças: {temp['numero_criancas']} \t Total de Pessoas: {temp['numero_adultos']+temp['numero_criancas']}")
        print (23*" * ")
        print("Dados de faturação:")
        print(f"Nome: {temp['nome_cliente']} com NIF: {temp['nif']}")
        print(f"Total a pagar: {temp['total_pagar']} euros\n")

        while not confirm:   
            resp = input("Deseja prosseguir com a reserva? (S/N) ")
            if resp =="s" or resp =="S" :
                meals.append(temp)
                guardarDados(meals,"meals.json")  
                print("Reserva efetuada com sucesso!")
                confirm = True               
            elif resp == "n" or resp =="N" :
                print("Reserva cancelada.")
                break    
            else:
                print("Caractere inválido! Insira S/N.")    
   
    return meals

#Função de validação do input do e-mail
def validacaoEmail(email):
    emailValido = False
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if(re.fullmatch(regex, email)):
        emailValido = True
    else:
         print("E-mail inválido! Insira novamente.")

    return emailValido

#Função de validação do input da data
def formatoData(dataPretendida):
    dataValida=False

    datetime.datetime.strptime(dataPretendida, "%Y-%m-%d")
    splitDate = dataPretendida.split('-')
    ano = int(splitDate[0])
    mes = int(splitDate[1])
    dia = int(splitDate[2])  

    # initialize data
    dataInserida = date(ano, mes, dia)
    data_atual = datetime.date.today()
    if dataInserida > data_atual:
        dataValida=True
    elif dataInserida < data_atual:
        print("Inseriu uma data inválida.")    
    else:
        print("Não pode seleccionar o próprio dia.")
    return dataValida    

#Função de verificação de data de fecho
def verificarFecho(dataPretendida, closedaysLD):
    diaFecho = False

    #ciclo for each para para percorrer lista de dicionarios de datas de fecho
    for item in closedaysLD:
        if item['dia_fecho'] == dataPretendida:
            diaFecho=True
            break
    return diaFecho

#Função de verificação do dia de folga
def diaFolga(dataPretendida, definitionsLD):
    folga = False
    #validação dia de folga
    dataObj = datetime.datetime.strptime(dataPretendida, "%Y-%m-%d")
    dia_semana = dataObj.strftime('%A')

    #ciclo for each para percorrer lista de dicionarios de reservas
    for item in definitionsLD:
        if item['dia_folga'] == dia_semana:
            folga=True
            break
    return folga


#Função para verificação da disponibilidade da data inserida
def verificarData(dataPretendida):
    dataValida=False
    diaFecho = False
    folga = False
    try:
        dataValida = formatoData(dataPretendida)
        diaFecho = verificarFecho(dataPretendida,closedaysLD)  
        folga = diaFolga(dataPretendida,definitionsLD)

        if diaFecho or folga:
            print("Nessa data estamos encerrados.")         

        #retorno da validação completa da data
        if dataValida and not diaFecho and not folga:
            return True    
        else:
            return False  
    except ValueError:
        print("ERRO! O formato da data deve ser do tipo aaaa-mm-dd")   
        return False

#Função de validação do input das horas
def validacaoHoras(horaPretendida):
    horasValidas = False
    try:
        #validação formato das horas
        time.strptime(horaPretendida, '%H:%M')
        if len(horaPretendida) == 5:   
            horasValidas = True   
            #validação horário de abertura
            horario = horarioRestaurante(horaPretendida, definitionsLD)

        if horasValidas and horario:
            return True
        else:
            return False          
    except ValueError:
        print("Formato de horas incorreto! Insira novamente.")
    return False

#Função de validação do horário de funcionamento do restaurante
def horarioRestaurante(horas, definitionsLD):

    #ciclo for each para percorrer lista de dicionarios de definições
    for item in definitionsLD:
        if horas >= item['abertura'] and horas < item['fecho']:
            return True
        else:
            print("Nesse horário estamos encerrados.")
            return False
    return False

#Função para verificar se reserva já foi efetuada
def reservaRepetida(dataPretendida, meals, email):
   
    lerFicheirosJson("meals.json")

    #ciclo for each para percorrer lista de dicionarios de reservas
    for item in meals:
        if item['email'] == email and dataPretendida == item['data']:
            print("Não foi possível efetuar a reserva:")
            print("Já tem uma reserva efetuada nessa data.")
            return True    
    return False

#Função de validação do número de pessoas
def totalPessoas(numAdultos, numCriancas, definitionsLD):
    if numAdultos > 12:
        print("No máximo 12 adultos por mesa.")
        return True

    if numAdultos < 0 or numCriancas <0:  
        print("Número de pessoas inválido!")
        return True

    for item in definitionsLD:
            if numAdultos + numCriancas >= item['ocupacao_maxima']:
                print("Pedimos desculpa! A lotação máxima do restaurante foi excedida.")
                return True
    return False


#Função de validação de nome
def validacaoNome(nome):
    padrao = r'^[a-zA-Z\s]+$'
    if re.match(padrao, nome):
        return True
    else:
        print("Nome inválido! Insira apenas letras e espaços.")
        return False


#Função de validação de NIF
def validacaoNif(nif):
    if len(nif) == 9 and nif.isnumeric() and nif[0] != '0':
        return True          
    else:
        print("NIF incorreto! Insira novamente")
        return False

#Funcao de cálculo do total a pagar
def totalPagamento(numAdultos,numCriancas,definitionsLD):
    for item in definitionsLD:
        total = (numAdultos*item['preco_adulto']) + (numCriancas*item['preco_crianca'])
    return total    


#Função do menu cliente - opção reserva mesa
def menuBookTable(email):    
    dataValida=False
    horaValida = False
    lotacao = True
    valNome = False
    valNif = False
    
    print("\n* * * * * * * Book Table * * * * * * *")
    while not dataValida:
        dataPretendida = input("Introduza a data no formato aaaa-mm-dd: ")
        dataValida = verificarData(dataPretendida)

    if dataValida:
        print("Horário: 19:00h às 22:00h")
        while not horaValida:
            horaPretendida = input("Introduza a hora prevista para a sua chegada no formato hh:mm : ")
            horaValida = validacaoHoras(horaPretendida)    

        if horaValida:
            print("Número de pessoas")
            while lotacao:
                numAdultos = int(input("Indique o número de pessoas (máx 12): "))
                numCriancas = int(input("Indique o número de crianças: "))
                lotacao = totalPessoas(numAdultos,numCriancas,definitionsLD)

            if not lotacao:
                print("Dados para a fatura")
                while not valNome:
                    nomeCliente = input("Insira o seu nome: ")
                    valNome = validacaoNome(nomeCliente)
                while not valNif:
                    nifCliente =  input("Insira o seu NIF: ")
                    valNif = validacaoNif(nifCliente)

                #Chamar função de reservas
                total = totalPagamento(numAdultos,numCriancas,definitionsLD)
                criarMeals(email, dataPretendida,horaPretendida, numAdultos, numCriancas, nomeCliente, nifCliente, total)
                


#Função de imprimir reservas
def imprimirReservas(email):
    
    print("\nHistórico de reservas do cliente:\n")
    for item in mealsLD:
        if item['email'] == email:  
            print(f"Data: {item['data']} \t Hora: {item['hora']}")
            print(f"Adultos: {item['numero_adultos']} \t Crianças: {item['numero_criancas']} \t Total de Pessoas: {item['numero_adultos']+item['numero_criancas']}")
            print(f"Nome: {item['nome_cliente']} com NIF: {item['nif']}")
            print(f"Total a pagar: {item['total_pagar']} euros\n")
            print (23*" * ")

#Função do menu cliente
def menuCliente(email):
    opValida = False
    while opValida == False:
        print("* * * * * * * Client Menu * * * * * * *")
        print("1 - Marcar Refeição")
        print("2 - Ver Histórico")
        print("3 - Sair")
        opCliente = int(input("Indique a opção desejada: "))
        if opCliente == 1 or opCliente == 2 or opCliente == 3:
            opValida = True

        match opCliente:
            case 1:
                menuBookTable(email)
                mealsLD = lerFicheirosJson("meals.json")
                menuCliente(email)  
            case 2:
                imprimirReservas(email)
                mealsLD = lerFicheirosJson("meals.json")
                menuCliente(email)
            case 3:
                print("Escolheu a opção sair. Até breve!")
                break    

#Função do menu administrador
def menuAdministrador(email):
    opValida = False
    teclaContinuar = False
    while not opValida or teclaContinuar:
        print("\n* * * * * * * Admin Menu * * * * * * *")
        print("1 - Definições")
        print("2 - Fecho dia")
        print("3 - Extrato reservas por dia")
        print("4 - Sair")
        opAdmin = int(input("Indique a opção desejada: "))
        if opAdmin == 1 or opAdmin == 2 or opAdmin == 3 or opAdmin == 4:
            opValida = True
 
        match opAdmin:
            case 1:
                menuDefinicoes(definitionsLD)
                teclaContinuar = True
                menuAdministrador(email)
                teclaContinuar = False
           
            case 2:
                menuFechoDia(definitionsLD)
                menuAdministrador(email)
                teclaContinuar = False
 
            case 3:
                
                menuExtratoReservas(definitionsLD, email)
                menuAdministrador(email)
                teclaContinuar = False
               
         
            case 4:
                print("Escolheu a opção sair!")
                break
                
 
    
 
 
#Função do menu administrador - opção definições
def menuDefinicoes(definitionsLD):  
    teclaContinuar= False
     
    print("\n* * * * * * * Definições: * * * * * * *")
    for item in definitionsLD:
        print(f"Preço por adulto: {item['preco_adulto']}")
        print(f"Preço por criança: {item['preco_crianca']}")
        print(f"Ocupação Máxima: {item['ocupacao_maxima']}")
        print(f"Número de mesas: {item['num_mesas_disponiveis']}")
        print(f"Dia de folga: {item['dia_folga']}")
 
    teclaContinuar = input("\nPor favor clique numa tecla para continuar ")
    teclaContinuar = True
 
 
#Função do menu administrador - opção fecho dia
def menuFechoDia(definitionsLD):
    dataFechoValida=False
    closedaysLD_sorted = sorted(closedaysLD, key=lambda x: x['dia_fecho'], reverse=True)
   
    print("\n* * * * * * * Fechos adicionados: * * * * * * *")
    for item in closedaysLD_sorted[:10]:
        print(f"Data de fecho: {item['dia_fecho']}")
   
    while not dataFechoValida:
        dataFechoPretendida=input("\nIntroduza o dia de fecho no formato aaaa-mm-dd: ")
        dataFechoValida=verificarDataFechoValida(dataFechoPretendida)
       
       
 
#Função para verificação da disponibilidade da data de fecho inserida
def verificarDataFechoValida(dataFechoPretendida):
    dataFechoValida=False
    diaFecho = False
    folga = False
    reservas= False
    try:
        dataFechoValida = formatoData(dataFechoPretendida)
        diaFecho = verificarFecho(dataFechoPretendida,closedaysLD)  
        folga = diaFolga(dataFechoPretendida,definitionsLD)
 
        if diaFecho or folga:
            print("Nessa data estamos encerrados. Esta data já se encontra registada")        
 
        #retorno da validação completa da data
        if dataFechoValida and not diaFecho and not folga:
            print("Dia de fecho inserido com sucesso!")
            closedaysLD.append({'dia_fecho': dataFechoPretendida})
            guardarDados(closedaysLD,"closedays.json")
           
            return True    
        else:
            return False  
    except ValueError:
        print("ERRO! O formato da data deve ser do tipo aaaa-mm-dd")  
        return False
   
 
#Função do menu administrador - opção extrato reservas
def menuExtratoReservas(definitionsLD, email):
    dataPesquisarValida=False
    
    while not dataPesquisarValida:
        dataPesquisarPretendida=input("\nIntroduza a data no formato aaaa-mm-dd: ")
        dataPesquisarValida=verificarDataPesquisarValida(dataPesquisarPretendida)
        
    imprimirReservasPorDia(dataPesquisarPretendida)
    estatisticas(dataPesquisarPretendida)
 
#Função para verificação data de pesquisa válida
def verificarDataPesquisarValida(dataPesquisarPretendida):
    dataPesquisarValida=False
    reservas= False
    try:
        dataPesquisarValida = formatoData(dataPesquisarPretendida)
        
        lerFicheirosJson("meals.json")

        for item in mealsLD:
            if dataPesquisarPretendida == item['data']:
                reservas= True
                            

        #retorno da validação completa da data
        if reservas:
            return True    
        else:
            print("Nessa data não tem nenhuma reserva!")
            return False  
            
    except ValueError:
        print("ERRO! O formato da data deve ser do tipo aaaa-mm-dd")  
        return False  

    #Função de imprimir reservas
def imprimirReservasPorDia(dataPesquisarPretendida):
    print(f"\n* * * * * * * Reservas adicionadas no dia : {dataPesquisarPretendida}* * * * * * *\n")
    
    
    for item in mealsLD:
        if item['data'] == dataPesquisarPretendida:  
            print(f"Data: {item['data']} \t Hora: {item['hora']}")
            print(f"Adultos: {item['numero_adultos']} \t Crianças: {item['numero_criancas']} \t Total de Pessoas: {item['numero_adultos']+item['numero_criancas']}")
            print(f"Nome: {item['nome_cliente']} com NIF: {item['nif']}")
            print(f"Total a pagar: {item['total_pagar']} euros\n")
            print (23*" * ")  
 

def estatisticas(dataPesquisarPretendida):
    print(f"\n* * * * * Estatísticas* * * * * * *\n")
    totalapagar=0
    totaldeAdultos=0
    totaldeCriancas=0
    totaldePessoas=0

    for item in mealsLD:
        if item['data'] == dataPesquisarPretendida:  
            totalapagar +=item['total_pagar']
            totaldeAdultos += item['numero_adultos']
            totaldeCriancas += item['numero_criancas']
            totaldePessoas += item['numero_adultos'] + item['numero_criancas']
        

    print(f"\nTotal faturado: {totalapagar} euros")
    print(f"\nTotal Adultos:  {totaldeAdultos} ")
    print(f"\nTotal Crianças: {totaldeCriancas}")
    print(f"\nTotal Pessoas: {totaldePessoas}\n")
    print (23*" * ")  



#Função de autenticação geral do user (cliente ou administrador)
def sistemaAutenticacao(usersLD):
    foundUser = False
    emailValido = False

    while not emailValido:
        print("* * * * * * * Autenticação * * * * * * *")
        email = input("Introduza o seu email: ")

        emailValido = validacaoEmail(email)

    #ciclo for each para percorrer lista de dicionarios de users
    for user in usersLD:
        if user['email'].lower() == email.lower():
            foundUser
            if user['permission'] == 'admin':
                password = input("Introduza a sua senha: ")
                if user['password'] == password:
                    print("Administrador autenticado com sucesso!")
                    #chamar função para mostrar menu do administrador
                    menuAdministrador(email)
                    return user
                else:
                    print("Autenticação falhou!")  
            else:
                print("Cliente autenticado com sucesso!")  
                #chamar função para mostrar menu do cliente
                menuCliente(email)
                return user
        
    #caso user não exista      
    if not foundUser:
        usersLD.append({'email': email, 'permission' :'client'})
        print("Cliente adicionado com sucesso!")
        #chamar função para guardar dados
        guardarDados(usersLD, "users.json")
        #chamar função para mostrar menu do cliente
        menuCliente(email)            

#Chamar função para criar definitions.json
criarDefinitions()

#Chamar função para criar users.json
criarUsers()

#Chamar função para criar closedays.json
criarCloseDays()

#Chamar função para fazer load dos ficheiros para listas de dicionários
definitionsLD = lerFicheirosJson("definitions.json")
usersLD = lerFicheirosJson("users.json")
closedaysLD = lerFicheirosJson("closedays.json")
mealsLD = lerFicheirosJson("meals.json")

#Chamar função autenticação
sistemaAutenticacao(usersLD)
