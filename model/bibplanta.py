from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base

# Classe para representar as plantas da biblioteca de plantas
class BibPlanta(Base):
    __tablename__ = 'bib_planta'

    id = Column("pk_planta", Integer, primary_key=True)
    nome = Column(String(60), unique=True)
    nome_cientifico = Column(String(100))
    nome_popular = Column(String(200))
    familia = Column(String(50))
    categoria = Column(String(100))
    clima = Column(String(50))
    origem = Column(String(50))
    altura = Column(String(50))
    luminosidade = Column(String(50))
    detalhamento = Column(String(200))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, nome_cientifico: str, nome_popular: str, categoria: str, clima: str, origem: str, altura: str,
                 luminosidade: str, familia: str, detalhamento: str, data_insercao: Union[DateTime, None] = None):
        
        """
        Cria uma instância de planta na biblioteca de plantas

        Arguments:
            nome: nome da planta
            nome_cientifico: nome cientifico da planta
            nome_popular: nome popular da planta
            familia: familia da planta
            categoria: classificação botânica da planta
            clima: clima no qual a planta desenvolve-se
            origem: país de origem da planta
            altura: porte da planta
            luminosidade: luminosidade exigida pela planta
            detalhamento: observações adicionais sobre a planta
            data_insercao: data de inserção da planta no banco de dados
        """
        self.nome = nome
        self.nome_cientifico = nome_cientifico
        self.nome_popular = nome_popular
        self.familia = familia
        self.categoria = categoria
        self.clima = clima
        self.origem = origem
        self.altura = altura
        self.luminosidade = luminosidade
        self.detalhamento = detalhamento

        # se não for informada, será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
