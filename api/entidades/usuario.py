#TODO usuario e Funcao/cargo juntas

class Usuario:
    def __init__(self, nome, email, senha, is_admin, status, cadastrado_em, atualizado_em, api_key,
                 cliente, funcao, producoes):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__is_admin = is_admin
        self.__status = status
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__api_key = api_key
        self.__cliente = cliente
        self.__funcao = funcao
        self.__producoes = producoes

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        self.__senha = senha

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        self.__is_admin = is_admin

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def cadastrado_em(self):
        return self.__cadastrado_em

    @cadastrado_em.setter
    def cadastrado_em(self, cadastrado_em):
        self.__cadastrado_em = cadastrado_em

    @property
    def atualizado_em(self):
        return self.__atualizado_em

    @atualizado_em.setter
    def atualizado_em(self, atualizado_em):
        self.__atualizado_em = atualizado_em

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key):
        self.__api_key = api_key

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente

    @property
    def funcao(self):
        return self.__funcao

    @funcao.setter
    def funcao(self, funcao):
        self.__funcao = funcao

    @property
    def producoes(self):
        return self.__producoes

    @producoes.setter
    def producoes(self, producoes):
        self.__producoes = producoes


#Entidade Funcao de Funcionarios
class Funcao:
    def __init__(self, nome, usuarios, cliente):
        self.__nome = nome
        self.__usuarios = usuarios
        self.__cliente = cliente

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def usuarios(self):
        return self.__usuarios

    @usuarios.setter
    def usuarios(self, usuarios):
        self.__usuarios = usuarios

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente
