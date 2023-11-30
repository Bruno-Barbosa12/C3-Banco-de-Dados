import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.clientes import Cliente
from model.ordem_servico import Ordem
from controller.controller_cliente import Controller_Cliente

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Ordem_Servico:
    
    def __init__(self):
        self.mongo = MongoQueries()
        self.ctrl_cliente = Controller_Cliente()
        self.relatorio = Relatorio()
        
    def inserir_ordem_servico(self) -> Ordem:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        # Lista os clientes existentes para inserir no pedido
        self.relatorio.get_relatorio_clientes()

        cpf = str(input("Digite o número do CPF do Cliente: "))
        
        if self.valida_cliente(cpf):
            cliente = self.valida_cliente(cpf)
        # Solicita os dados da ordem de serviço
            cpf_cliente = cliente.get_cpf()  # Aqui está corrigido para obter o CPF do cliente
            item = input("Item: ")
            defeito = input("Defeito apresentado: ")
            status = input("Status(Novo): ")
            preco = float(input(f"Informe o preço do serviço: "))
            data_hoje = datetime.today().strftime("%m-%d-%Y")
        
            # Encontrar o maior código de ordem atual
            maior_codigo_ordem = self.mongo.db["ordem_servico"].find_one(sort=[("codigo_ordem", -1)])

            # Se houver um maior código de ordem, adicione 1 a ele, caso contrário, defina como 1
            proximo_codigo_ordem = 1
            
            if maior_codigo_ordem:
                proximo_codigo_ordem = maior_codigo_ordem["codigo_ordem"] + 1

             # Insere e persiste o novo ordem servico
            data = dict(codigo_ordem=proximo_codigo_ordem, data=data_hoje, cpf=cliente.get_cpf(),item=item,defeito=defeito,status=status,preco=preco)
            id_ordem = self.mongo.db["ordem_servico"].insert_one(data)

            df_ordem = self.recupera_ordem(id_ordem.inserted_id)
            
            # Cria um novo objeto Ordem
            nova_ordem_servico= Ordem(df_ordem.codigo_ordem.values[0], df_ordem.data.values[0], df_ordem.cpf.values[0],df_ordem.item.values[0],df_ordem.defeito.values[0],df_ordem.status.values[0], df_ordem.preco.values[0])
            # Exibe os atributos do novo produto
            print(nova_ordem_servico.to_string())
            self.mongo.close()
            return nova_ordem_servico
        
    def atualizar_ordem(self) -> Ordem:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código da ordem de serviço a ser alterado
        codigo_ordem = int(input("Código da ordem de serviço que irá alterar: "))        

        # Verifica se a ordem existe na base de dados
        if not self.verifica_existencia_ordem(codigo_ordem):
            
            item = input("Item: ")
            defeito = input("Defeito apresentado: ")
            status = input("Status(Novo): ")
            preco = float(input(f"Informe o preço do serviço: "))

            # Atualiza a descrição da ordem de serviço existente
            self.mongo.db["ordem_servico"].update_one({"codigo_ordem": codigo_ordem}, {"$set": {"item": item, "defeito" : defeito, "status" : status, "preco" : preco}})

            # Recupera os dados do nova ordem criada transformando em um DataFrame
            df_ordem= self.recupera_ordem_codigo(codigo_ordem)
            # Cria um novo objeto Produto
            ordem_atualizada = Ordem(df_ordem.codigo_ordem.values[0], df_ordem.data.values[0], df_ordem.cpf.values[0],df_ordem.item.values[0],df_ordem.defeito.values[0],df_ordem.status.values[0], df_ordem.preco.values[0])
            # Exibe os atributos do novo produto
            print(ordem_atualizada.to_string())
            self.mongo.close()
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return ordem_atualizada
        else:
            self.mongo.close()
            print(f"O código {codigo_ordem} não existe.")
            return None
        
    def excluir_pedido(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        self.relatorio.get_relatorio_ordem_servico()
        
        # Solicita ao usuário o código da ordem de serviço a ser excluido
        codigo_ordem = int(input("Código da ordem de serviço que irá excluir: "))        

        # Verifica se a ordem existe na base de dados
        if not self.verifica_existencia_ordem(codigo_ordem):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_ordem = self.recupera_ordem_codigo(codigo_ordem)
            
            opcao_excluir = input(f"Tem certeza que deseja excluir a ordem de serviço {codigo_ordem} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    self.mongo.db["ordem_servico"].delete_one({"codigo_ordem": codigo_ordem})
                    print("Ordem do pedido removido com sucesso!")
                    # Cria um novo objeto Produto para informar que foi removido
                    ordem_excluida= Ordem(df_ordem.codigo_ordem.values[0], df_ordem.data.values[0], df_ordem.cpf.values[0],df_ordem.item.values[0],df_ordem.defeito.values[0],df_ordem.status.values[0], df_ordem.preco.values[0])
                    self.mongo.close()
                    # Exibe os atributos do produto excluído
                    print("Pedido Removido com Sucesso!")
                    return ordem_excluida
                    print(ordem_excluida.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_ordem} não existe.")
        
        
    

    def verifica_existencia_ordem(self, codigo:int=None, external: bool = False) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_ordem = self.recupera_ordem_codigo(codigo=codigo, external=external)
        return df_ordem.empty
    
    def recupera_ordem(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_ordem = pd.DataFrame(list(self.mongo.db["ordem_servico"].find({"_id":_id}, {"codigo_ordem": 1, "data": 1, "cpf": 1, "item": 1, "defeito": 1,"status": 1,"preco": 1,"_id": 0})))
        return df_ordem
     

    def recupera_ordem_codigo(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_ordem= pd.DataFrame(list(self.mongo.db["ordem_servico"].find({"codigo_ordem": codigo},{"codigo_ordem": 1, "data": 1, "cpf": 1, "item": 1, "defeito": 1,"status": 1,"preco": 1,"_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_ordem

    def valida_cliente(self, cpf:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(cpf=cpf, external=True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.ctrl_cliente.recupera_cliente(cpf=cpf, external=True)
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0], df_cliente.telefone.values[0], df_cliente.endereco.values[0])
            return cliente