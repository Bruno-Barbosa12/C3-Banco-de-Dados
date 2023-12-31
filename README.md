# Sistema de Gerenciamento de Ordens de Serviço em Python com MongoDB

Este sistema exemplifica a gestão de ordens de serviço, com coleções que representam clientes e as ordens de serviços associadas a eles.

Para iniciar o sistema e criar as coleções com dados de exemplo no MongoDB, execute o seguinte comando no terminal:

```shell
~$ python createCollectionsAndData.py

Para utilizar o sistema, execute o seguinte comando no terminal:

~$ python main.py

Organização do Sistema:

O sistema possui duas entidades: Clientes e Ordem

diagrams: Este diretório contém o [diagrama do banco de dados](Diagrama Ordem.png), que ilustra a estrutura das coleções de clientes e ordens de serviço.

src: Este diretório contém os scripts do sistema.
db_connection: Aqui está os módulos de conexão com o MongoDB, que incluem funcionalidades úteis para a execução de operações CRUD.

Exemplo de consulta de clientes no MongoDB:

from db_connection.mongo_queries import MongoQueries

models: Este diretório contém as classes que representam os dados das coleções.

controllers: Este diretório contém as classes responsáveis por manipular os dados das coleções.

utils: Este diretório contém scripts úteis para o sistema, como configurações e funções auxiliares.

createCollectionsAndData.py: Script para criar e preencher as coleções no MongoDB. Deve ser executado antes de iniciar o sistema.

main.py: Script principal que atua como interface do usuário para o sistema de gerenciamento de ordens de serviço.

O trabalho foi testado e executado na máquina virtual criada pelo professor da disciplina de Banco de Dados: Howard Roatti 
