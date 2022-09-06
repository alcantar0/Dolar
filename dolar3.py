# coding=utf-8
from datetime import date
import requests
from bs4 import BeautifulSoup

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()


class Dados(Base):
    __tablename__ = "dados"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    data = Column(String)
    valor = Column(Float)


engine = create_engine("postgresql+psycopg2://pedro:qwe123@localhost/dados")

Base.metadata.create_all(engine)

meses = {
    "jan": "01",
    "fev": "02",
    "mar": "03",
    "abr": "04",
    "mai": "05",
    "jun": "06",
    "jul": "07",
    "ago": "08",
    "set": "09",
    "out": "10",
    "nov": "11",
    "dez": "12",
}
mes = str(input("Qual mês? basta digitar as primeiras três letras do mês: "))

# Web-Scraping
def get_website_data():
    definir_site = requests.get("https://dolarhoje.com")
    funcao_de_funcionamento = BeautifulSoup(definir_site.content, "html.parser")
    procurar_linha = funcao_de_funcionamento.find(id="nacional")
    linha_convertida_para_caracteres = str(procurar_linha)

    # Converte de str pra float
    valor_em_real = linha_convertida_para_caracteres[-7:-3]

    valor_em_real = valor_em_real.replace(",", ".")
    valor_em_real = float(valor_em_real)

    return valor_em_real


def connect_retrieve_and_post_data_on_db():
    with Session(engine) as session:
        today = date.today()
        results = session.query(Dados).filter_by(data=str(today)).all()
        if len(results) == 0:
            valor = get_website_data()
            dados = Dados(data=today, valor=valor)
            session.add(dados)
            session.commit()
        else:
            print("Dados de hoje já enviados ao banco de dados.")


def plot_graph():
    dias = []
    valores = []
    with Session(engine) as session:
        s_dias = session.query(Dados.data).all()
        s_valores = session.query(Dados.valor).all()
        for dia in s_dias:
            dia = str(dia)
            print(dia)
            if dia[7:9] == meses[mes]:
                dias.append(dia[10:12])
        for valor in s_valores:
            valor = str(valor)
            valor = valor.replace(",", ".")
            valor = float(valor[1:5])
            valores.append(valor)
    import matplotlib.pyplot as plt
    plt.plot(dias, valores)
    plt.show()
    print(dias)
    print(valores)


print(f"UM DOLAR EM REAIS ESTÁ VALENDO HOJE: :  {get_website_data()} REAIS")
connect_retrieve_and_post_data_on_db()
plot_graph()
from time import sleep

sleep(1)
