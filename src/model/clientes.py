class Cliente: 
    def __init__(self, 
                 cpf:str=None, 
                 nome:str=None,
                 telefone:str=None,
                 endereco:str=None,
                ):
        self.set_cpf(cpf)
        self.set_nome(nome)
        self.set_telefone(telefone)
        self.set_endereco(endereco)
        

    def set_cpf(self, cpf:str):
        self.cpf = cpf

    def set_nome(self, nome:str):
        self.nome = nome

    def set_telefone(self, telefone:str):
        self.telefone = telefone

    def set_endereco(self, endereco:str):
        self.endereco = endereco

    def get_cpf(self) -> str:
        return self.cpf

    def get_nome(self) -> str:
        return self.nome
    
    def get_telefone(self) -> str:
        return self.telefone
    
    def get_endereco(self) -> str:
        return self.endereco

    def to_string(self) -> str:
        return f"CPF: {self.get_cpf()} | Nome: {self.get_nome()} | Telefone: {self.get_telefone()} | Endereco: {self.get_endereco()}"
