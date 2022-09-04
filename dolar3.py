# coding=utf-8
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from datetime import date
#import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import psycopg2


meses={
        "jan":"01",
        "fev":"02",
        "mar":"03",
        "abr":"04",
        "mai":"05",
        "jun":"06",
        "jul":"07",
        "ago":"08",
        "set":"09",
        "out":"10",
        "nov":"11",
        "dez":"12"
} 
mes=str(input("Qual mês? basta digitar as primeiras três letras do mês: "))

def get_website_data():
        definir_site=requests.get('https://dolarhoje.com')
        funcao_de_funcionamento = BeautifulSoup(definir_site.content, 'html.parser')
        procurar_linha = funcao_de_funcionamento.find(id = 'nacional')
        linha_convertida_para_caracteres=str(procurar_linha)

        #Converte de str pra float
        valor_em_real=(linha_convertida_para_caracteres[-7:-3])

        valor_em_real=valor_em_real.replace(",", ".")
        valor_em_real=float(valor_em_real)

        return valor_em_real

def connect_and_retrieve_data():
        conn = psycopg2.connect(database="dados", user='pedro', 
        password='qwe123', host='localhost', port= '5432')
        today = date.today()
        conn.autocommit = True 
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(1) FROM dados WHERE dia = '{today}';")
        fetch_test = cursor.fetchone()
        if fetch_test[0] == 0:
                sql=('''INSERT INTO dados VALUES (%s, %s)''')
                valor = get_website_data()
                val= (today, valor)
                cursor.execute(sql, val)
        else:
                print("Dados de hoje já enviados ao banco de dados.")
def plot_graph():
        conn = psycopg2.connect(database="dados", user='pedro', 
        password='qwe123', host='localhost', port= '5432')
        conn.autocommit = True 
        cursor = conn.cursor()   
        select_query='SELECT * FROM dados;'
        cursor.execute(select_query)
        records=cursor.fetchall()
        print(records)
        dia=[]
        valores=[]
        for row in records:
                string_dias=str(row[0])
                string_dolares=str(row[1])
                while (string_dias[5:7]) == meses[mes]:
                        strin2=string_dias.replace(",", ".")
                        dia.append(string_dias[8:10])
                        valores.append(float(string_dolares[0:4]))
                        break
        print(dia)
        print(valores)
        plt.plot(dia, valores)
        plt.xlabel("Dia do mês")
        plt.ylabel("Valor do dólar em real")
        plt.title(f"Dólar no mês de {meses[mes]}")
        plt.show()

print(f'UM DOLAR EM REAIS ESTÁ VALENDO HOJE: :  {get_website_data()} REAIS')
connect_and_retrieve_data()
plot_graph()
from time import sleep
sleep(1)
