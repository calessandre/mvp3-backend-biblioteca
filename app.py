from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from model import Session, BibPlanta
from schemas import *
from sqlalchemy import update, func
import requests, json
from datetime import datetime

info = Info(title="API para gerenciamento de biblioteca de plantas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Documentação da API.")
bibplanta_tag = Tag(name="API", description="Adição, visualização e remoção de plantas na biblioteca.")

#############################
# Implementando as rotas
#############################

# Rota para DOCUMENTAÇÃO swagger
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger - abre a documentação swagger da API proposta.
    """
    return redirect('/openapi/swagger')

# Rota para ADICIONAR planta (POST)
@app.post('/bibplanta', tags=[bibplanta_tag],
          responses={"200": BibPlantaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_planta(form: BibPlantaSchema):
    """Adiciona uma nova planta e retorna uma representação da planta.
    """

    dt_insercao = datetime.now();
    data_e_hora_em_texto = "27/05/1979 00:00"
    data_e_hora = datetime.strptime(data_e_hora_em_texto, "%d/%m/%Y %H:%M")

    # Buscando a data e hora na API Externa para armazenar posteriormente no banco de dados
    response = requests.get('https://tools.aimylogic.com/api/now?tz=America/Sao_Paulo&format=dd/MM/yyyy%20HH:mm')
    resposta = json.loads(response.content)
    data_formatada = resposta['formatted']
    data_e_hora = datetime.strptime(data_formatada, "%d/%m/%Y %H:%M")

    bibplanta = BibPlanta(
        nome=form.nome,
        nome_cientifico=form.nome_cientifico,
        nome_popular=form.nome_popular,
        familia=form.familia,
        categoria=form.categoria,
        clima = form.clima,
        origem=form.origem,
        altura=form.altura,
        luminosidade=form.luminosidade,
        detalhamento=form.detalhamento,
        data_insercao=data_e_hora
        )

    try:
        # criando conexão com a base de dados
        session = Session()
        # adicionando planta
        session.add(bibplanta)
        # efetivando o comando de inclusão de nova planta na tabela
        session.commit()
        return apresenta_plantabib(bibplanta), 200

    except IntegrityError as e:
        # retorna erro caso já haja planta com mesmo nome cadastrada na tabela ou outro erro de integridade
        error_msg = "Planta de mesmo nome já salva na base."
        return {"message": error_msg}, 409

    except Exception as e:
        # caso ocorra um erro diferente dos anteriores
        error_msg = "Não foi possível salvar novo item."
        return {"message": error_msg}, 400


# Rota para BUSCAR TODAS as plantas cadastradas (GET)
@app.get('/bibplantas', tags=[bibplanta_tag],
         responses={"200": ListagemBibPlantasSchema, "404": ErrorSchema})
def get_plantas():
    """Faz a busca por todos as plantas cadastradas e retorna uma representação da listagem de plantas.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    plantas = session.query(BibPlanta).all()

    if not plantas:
        # se não há plantas cadastradas
        return {"plantas": []}, 200
    else:
        # retorna a representação de planta
        #print(plantas)
        return apresenta_plantasbib(plantas), 200


# Rota para APAGAR uma planta pelo id (DELETE).
@app.delete('/bibplanta', tags=[bibplanta_tag],
            responses={"200": BibPlantaDelUpdtSchema, "404": ErrorSchema})
def del_planta(query: BibPlantaBuscaIdSchema):
    """Deleta uma planta a partir do id informado e retorna uma mensagem de confirmação da remoção.
    """
    planta_id = query.planta_id

    # criando conexão com a base
    session = Session()
    
    # fazendo a remoção
    count = session.query(BibPlanta).filter(BibPlanta.id == planta_id).delete()
    
    # commitando as alterações
    session.commit()

    if count:
        # retorna a mensagem de confirmação e o id da planta removida
        return {"message": "Planta removida.", "id": planta_id}
    else:
        # se a planta não foi encontrada, retorna mensagem de erro
        error_msg = "Planta não encontrada na base."
        return {"message": error_msg}, 404


# Rota para BUSCAR UMA planta pelo nome (GET)
@app.get('/bibplanta', tags=[bibplanta_tag],
         responses={"200": BibPlantaViewSchema, "404": ErrorSchema})
def get_planta(query: BibPlantaBuscaNomeSchema):
    """Faz a busca por um planta a partir do nome da planta e retorna uma representação da planta.
    """
    planta_nome = query.planta_nome
    
    # criando conexão com a base
    session = Session()

    # fazendo a busca (sem considerar maiúsculas ou minúsculas)
    planta = session.query(BibPlanta).filter(func.upper(BibPlanta.nome) == func.upper(planta_nome)).first()

    if not planta:
        # se a planta não foi encontrada
        error_msg = "Planta nao encontrada na base."
        return {"message": error_msg}, 404
    else:
        # retorna a representação de planta
        return apresenta_plantabib(planta), 200
    

# Rota para ATUALIZAR uma planta pelo id (PUT).
@app.put('/bibplanta', tags=[bibplanta_tag],
            responses={"200": BibPlantaDelUpdtSchema, "404": ErrorSchema})
def updt_planta(query: BibPlantaBuscaIdSchema, form: BibPlantaSchema):
    """Atualiza uma planta a partir do id informado e retorna uma mensagem de confirmação da remoção.
    """
    planta_id = query.planta_id

    # criando conexão com a base
    session = Session()
    
    # fazendo a atualização
    count = session.query(BibPlanta).filter(BibPlanta.id == planta_id).update({BibPlanta.nome: form.nome,
                            BibPlanta.nome_cientifico: form.nome_cientifico,
                            BibPlanta.nome_popular: form.nome_popular,
                            BibPlanta.familia: form.familia,
                            BibPlanta.categoria: form.categoria,
                            BibPlanta.clima: form.clima,
                            BibPlanta.origem: form.origem,
                            BibPlanta.altura: form.altura,
                            BibPlanta.luminosidade: form.luminosidade,
                            BibPlanta.detalhamento: form.detalhamento
                        })
    
    # commitando as alterações
    session.commit()

    if count:
        # retorna a mensagem de confirmação e o id da planta atualizada
        return {"message": "Planta atualizada com sucesso.", "id": planta_id}
    else:
        # se a planta não foi encontrada, retorna mensagem de erro
        error_msg = "Planta não encontrada na base."
        return {"message": error_msg}, 404
    
 #############################

# Rota para teste de CHAMADA DE API externa
@app.get('/testeAPIExt', tags=[bibplanta_tag])
def testeAPIExt():
    response = requests.get('https://tools.aimylogic.com/api/now?tz=America/Sao_Paulo&format=dd/MM/yyyy%20HH:mm:ss')
    
    #print (response.text)
    #print (response.status_code)
    #print(response.content)
    
    return (response.content)
