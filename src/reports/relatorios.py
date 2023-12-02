from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass
    
    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["cliente"].find({}, 
                                                 {"cpf": 1, 
                                                  "nome": 1, 
                                                  "telefone": 1, 
                                                  "endereco": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_cliente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_cliente)
        input("Pressione Enter para Sair do Relatório de Clientes")
    
    def get_relatorio_ordem_servico(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["ordem_servico"].find({}, 
                                                    {"codigo_ordem": 1, 
                                                    "data": 1, 
                                                    "cpf": 1, 
                                                    "item": 1, 
                                                    "defeito": 1, 
                                                    "status": 1, 
                                                    "preco": 1, 
                                                    "_id": 0
                                                    }).sort("codigo_ordem", ASCENDING)
        df_ordem_servico = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_ordem_servico)
        input("Pressione Enter para Sair do Relatório de Ordem de Serviço")

    def get_ordens_servico_por_cpf(self, cpf):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()

        pipeline = [
            {
                '$match': {
                    'cpf': cpf  # CPF do cliente que deseja buscar
                }
            },
            {
                '$lookup': {
                    'from': 'clientes',  # Coleção de clientes
                    'localField': 'cpf',  # Campo na coleção ordem_servico
                    'foreignField': 'cpf',  # Campo na coleção clientes
                    'as': 'cliente_info'  # Alias para o resultado do lookup
                }
            },
            {
                '$unwind': '$cliente_info'  # Se o resultado for um array, desagrupa
            },
            {
                '$project': {  # Projeta os campos desejados
                    'codigo_ordem': 1,
                    'data': 1,
                    'cpf': 1,
                    'item': 1,
                    'defeito': 1,
                    'status': 1,
                    'preco': 1,
                    '_id': 0
                }
            },
            {
                '$sort': {'data': 1}  # Ordena por data ascendente
            }
        ]

        # Executa a agregação com o pipeline definido
        ordens_por_cpf = mongo.db["ordem_servico"].aggregate(pipeline)

        # Converte o resultado para um DataFrame se necessário
        df_ordens_servico_cpf = pd.DataFrame(list(ordens_por_cpf))

        # Verifica se há ordens de serviço associadas ao cliente
        if not df_ordens_servico_cpf.empty:
            print("Ordens de serviço associadas ao cliente:")
            print(df_ordens_servico_cpf)
        else:
            print(f"Não existem ordens de serviço associadas ao CPF {cpf}.")

        # Fecha a conexão com o MongoDB
        mongo.close()

        # Retorna o DataFrame com as ordens de serviço do CPF fornecido
        return df_ordens_servico_cpf

    def get_ordem_servico_por_codigo(self):
         # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()

        codigo_ordem = int(input("Digite o código da ordem de serviço para buscar: "))

        # Verifica se a ordem de serviço existe
        ordem_existe = mongo.db["ordem_servico"].find_one({"codigo_ordem": codigo_ordem})

        if ordem_existe:
            
            # Recupera os dados transformando em um DataFrame
            query_result = mongo.db["ordem_servico"].find({"codigo_ordem": codigo_ordem}, 
                                                        {"codigo_ordem": 1, 
                                                        "data": 1, 
                                                        "cpf": 1, 
                                                        "item": 1, 
                                                        "defeito": 1, 
                                                        "status": 1, 
                                                        "preco": 1, 
                                                        "_id": 0
                                                        }).sort("data", ASCENDING)
            df_ordem_servico_codigo = pd.DataFrame(list(query_result))
            # Fecha a conexão com o mongo
            mongo.close()
            # Retorna o DataFrame com a ordem de serviço do código fornecido
            print(df_ordem_servico_codigo)
            input("Pressione Enter para Sair do Relatório de Ordens de Serviço")
        else:
            print(f"O código de ordem de serviço {codigo_ordem} não está cadastrado.")
            return None  # Ou qualquer ação que você queira realizar em caso de código não cadastrado

    
    def get_ordem_servico_por_status(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()

        # Recebe o status como entrada
        status = input("Digite o status para buscar as ordens de serviço: ")

        # Verifica se existem ordens de serviço com o status fornecido
        ordens_com_status = mongo.db["ordem_servico"].find({"status": status}, {"_id": 0})

        # Transforma o cursor em uma lista para verificar o comprimento
        ordens_list = list(ordens_com_status)

        if len(ordens_list) > 0:
            # Exibe as ordens de serviço com o status fornecido
            print(f"Ordens de serviço com o status '{status}':")
            for ordem in ordens_list:
                print(ordem)
        else:
            print(f"Nenhuma ordem de serviço encontrada com o status '{status}'.")

        input("Pressione Enter para Sair do Relatório de Ordens de Serviço")
        # Fecha a conexão com o banco
        mongo.close()

        
    def get_defeitos_por_item(self):
    # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()

        # Recebe o item como entrada
        item = input("Digite o item para buscar os defeitos: ")

        # Busca os defeitos para o item fornecido
        ordens_servico = mongo.db["ordem_servico"].find({"item": item}, {"_id": 0, "defeito": 1})

        # Verifica se há resultados
        if ordens_servico.alive:
            # Exibe os defeitos para o item fornecido
            print(f"Defeitos relacionados ao item '{item}':")
            for ordem in ordens_servico:
                print(ordem["defeito"])
        else:
            print(f"Nenhum defeito encontrado para o item '{item}'.")

        input("Pressione Enter para Sair do Relatório de Ordens de Serviço")
        # Fecha a conexão com o banco
        mongo.close()
    
    def get_quantidade_status(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()

        pipeline = [
            {
                '$group': {
                    '_id': '$status',  # Campo pelo qual deseja agrupar
                    'total': {'$sum': 1}  # Contador de registros para cada status
                }
            },
            {
                '$sort': {'_id': 1}  # Ordena os resultados por status
            }
        ]

        # Executa a operação de agregação com o pipeline definido
        status_agregados = mongo.db["ordem_servico"].aggregate(pipeline)

        # Imprime os resultados
        print("Agrupamento por status:")
        for status in status_agregados:
            print(f"Status: {status['_id']} - Total: {status['total']}")

        input("Pressione Enter para Sair do Relatório de Ordens de Serviço")
        
        # Fecha a conexão com o MongoDB
        mongo.close()
