import pandas as pd
from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries
from reports.relatorios import Relatorio

class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo Documento
        cpf = input("Cpf (Novo): ")

        if self.verifica_existencia_cliente(cpf):
            # Solicita mais dados do usuário
            nome = input("Nome (Novo): ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            # Insere e persiste o novo cliente
            self.mongo.db["cliente"].insert_one({"cpf": cpf, "nome": nome, "telefone": telefone, "endereco": endereco})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0],df_cliente.telefone.values[0],df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            self.mongo.close()
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Lista os clientes existentes para inserir no pedido
        self.relatorio.get_relatorio_clientes()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = input("CPF do cliente que deseja alterar o nome: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpf):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            novo_telefone = input("Telefone: ")
            novo_endereco = input("Endereço: ")
            # Atualiza o nome do cliente existente
            self.mongo.db["cliente"].update_one({"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome, "telefone" : novo_telefone, "endereco" : novo_endereco}})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0],df_cliente.telefone.values[0],df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Lista os clientes existentes para inserir no pedido
        self.relatorio.get_relatorio_clientes()

        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = input("CPF do Cliente que irá excluir: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpf): 
            if self.verifica_associacao_ordem_servico(cpf):
                print("Não é possível excluir. O CPF está associado a ordens de serviço.")
            else:               
                # Recupera os dados do novo cliente criado transformando em um DataFrame
                df_cliente = self.recupera_cliente(cpf)
                opcao_excluir = input(f"Tem certeza que deseja excluir o cliente {cpf} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o cliente da tabela
                    self.mongo.db["cliente"].delete_one({"cpf":f"{cpf}"})
                    # Cria um novo objeto Cliente para informar que foi removido
                    cliente_excluido = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0],df_cliente.telefone.values[0],df_cliente.endereco.values[0])
                    print("Cliente Removido com Sucesso!")
                    print(cliente_excluido.to_string())
            self.mongo.close()
            # Exibe os atributos do cliente excluído
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")



    def verifica_associacao_ordem_servico(self, cpf):
        #   Consulta se o CPF do cliente está presente na tabela ordem_servico
        count = self.mongo.db["ordem_servico"].count_documents({"cpf": f"{cpf}"})
        return count > 0  # Retorna True se há associação, False se não há

    def verifica_existencia_cliente(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(self.mongo.db["cliente"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "telefone": 1, "endereco": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente.empty

    def recupera_cliente(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["cliente"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "telefone": 1, "endereco": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente