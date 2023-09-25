from pydantic import BaseModel
from typing import Optional, List
from model.bibplanta import BibPlanta

class BibPlantaSchema(BaseModel):
    """ Define como uma nova planta a ser inserida na base deve ser representada.
    """
    nome: str = "Anturio"
    nome_cientifico: str = "Anthurium andraeanum"
    nome_popular: str = "flor-verniz"
    familia: str = "Araceae"
    categoria: str = "Flores Perenes, Forrações à Meia Sombra"
    clima: str = "Equatorial, Subtropical, Tropical"
    origem: str = "América do Sul"
    altura: str = "0,3m a 0,6m"
    luminosidade: str = "meia sombra"
    detalhamento: str = "Exemplo de detalhamento da planta na biblioteca de plantas"

class BibPlantaBuscaIdSchema(BaseModel):
    """ Define como será a estrutura que representa a busca de uma planta pelo seu id.
    """
    planta_id: int = 1

class BibPlantaBuscaNomeSchema(BaseModel):
    """ Define como será a estrutura que representa a busca de uma planta pelo seu id.
    """
    planta_nome: str = "Anturio"


def apresenta_plantasbib(plantas: List[BibPlanta]):
    """ Retorna uma representação de plantas seguindo o schema definido em PlantaViewSchema.
    """
    result = []
    for planta in plantas:
        result.append({
            "id": planta.id,
            "nome": planta.nome,
            "nome_cientifico": planta.nome_cientifico,
            "nome_popular": planta.nome_popular,
            "familia": planta.familia,
            "categoria": planta.categoria,
            "clima": planta.clima,
            "origem": planta.origem,
            "altura": planta.altura,
            "luminosidade": planta.luminosidade,
            "detalhamento": planta.detalhamento
        })

    return {"plantas": result}


class BibPlantaViewSchema(BaseModel):
    """ Define como uma planta será retornada.
    """
    id: int = 1
    nome: str = "Anturio"
    nome_cientifico: str = "Anthurium andraeanum"
    nome_popular: str = "flor-verniz"
    familia: str = "Araceae"
    categoria: str = "Flores Perenes, Forrações à Meia Sombra"
    clima: str = "Equatorial, Subtropical, Tropical"
    origem: str = "América do Sul"
    altura: str = "0,3m a 0,6m"
    luminosidade: str = "meia sombra"
    detalhamento: str = "Exemplo de detalhamento da planta na biblioteca de plantas"

class BibPlantaDelUpdtSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção de uma planta.
    """
    message: str
    id: int

def apresenta_plantabib(planta: BibPlanta):
    """ Retorna uma representação da planta seguindo o schema definido em PlantaViewSchema.
    """
    return {
        "id": planta.id,
        "nome": planta.nome,
        "nome_cientifico": planta.nome_cientifico,
        "nome_popular": planta.nome_popular,
        "familia": planta.familia,
        "categoria": planta.categoria,
        "clima": planta.clima,
        "origem": planta.origem,
        "altura": planta.altura,
        "luminosidade": planta.luminosidade,
        "detalhamento": planta.detalhamento
    }

class ListagemBibPlantasSchema(BaseModel):
    """ Define como uma listagem de plantas será retornada.
    """
    plantas:List[BibPlantaViewSchema]
    