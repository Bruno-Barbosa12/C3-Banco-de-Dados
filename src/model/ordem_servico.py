from datetime import date

class Ordem:
    def __init__(self, 
                 cod_ordem: str = None,
                 data_ordem: date = None,
                 cpf_cliente: str = None,
                 item: str = None,
                 defeito: str = None,
                 status: str = None,
                 preco: float = None,
                 ):
        
        self.set_cod_ordem(cod_ordem)
        self.set_data_ordem(data_ordem)
        self.set_cpf_cliente(cpf_cliente)
        self.set_item(item)
        self.set_defeito(defeito)
        self.set_status(status)
        self.set_preco(preco)

    def set_cod_ordem(self, cod_ordem: str):
        self.cod_ordem = cod_ordem
    
    def set_cpf_cliente(self, cpf_cliente: str):
        self.cpf_cliente = cpf_cliente

    def set_defeito(self, defeito: str):
        self.defeito = defeito    

    def set_data_ordem(self, data_ordem: date):
        self.data_ordem = data_ordem

    def set_status(self, status: str):
        self.status = status

    def set_preco(self, preco: float):
        self.preco = preco

    def set_item(self, item: str):
        self.item = item

    def get_cod_ordem(self) -> str:
        return self.cod_ordem
      
    def get_cpf_cliente(self) -> str:
        return self.cpf_cliente
    
    def get_defeito(self) -> str:
        return self.defeito

    def get_data_ordem(self) -> date:
        return self.data_ordem

    def get_status(self) -> str:
        return self.status
    
    def get_preco(self) -> float:
        return self.preco

    def get_item(self) -> str:
        return self.item

    def to_string(self) -> str:
        return f"Codigo da ordem: {self.get_cod_ordem()} | CPF do cliente: {self.get_cpf_cliente()} | Defeito: {self.get_defeito()} | Data da Ordem: {self.get_data_ordem()} | Status: {self.get_status()} | Preço: {self.get_preco()} | Item: {self.get_item()}"
