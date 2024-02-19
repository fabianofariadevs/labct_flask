
class Cliente:
    def __init__(self, nome, endereco, bairro, cidade, estado, telefone, email, responsavel, whatsapp, cnpj, status,
                 filiais, cadastrado_em, atualizado_em, receitas, pedido_compra, pedidos_prod, usuarios, estoques):
        self.__nome = nome
        self.__endereco = endereco
        self.__bairro = bairro
        self.__cidade = cidade
        self.__estado = estado
        self.__telefone = telefone
        self.__email = email
        self.__responsavel = responsavel
        self.__whatsapp = whatsapp
        self.__cnpj = cnpj
        self.__status = status
        self.__filiais = filiais
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__receitas = receitas
        self.__pedidos_compra = pedido_compra
        self.__pedidos_prod = pedidos_prod
        self.__usuarios = usuarios
        self.__estoques = estoques

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco

    @property
    def bairro(self):
        return self.__bairro

    @bairro.setter
    def bairro(self, bairro):
        self.__bairro = bairro

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        self.__estado = estado

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def responsavel(self):
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel):
        self.__responsavel = responsavel

    @property
    def whatsapp(self):
        return self.__whatsapp

    @whatsapp.setter
    def whatsapp(self, whatsapp):
        self.__whatsapp = whatsapp

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        self.__cnpj = cnpj

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def filiais(self):
        return self.__filiais

    @filiais.setter
    def filiais(self, filiais):
        self.__filiais = filiais

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
    def receitas(self):
        return self.__receitas

    @receitas.setter
    def receitas(self, receitas):
        self.__receitas = receitas

    @property
    def pedidosprod(self):
        return self.__pedidosprod

    @pedidosprod.setter
    def pedidosprod(self, pedidosprod):
        self.__pedidosprod = pedidosprod

    @property
    def pedido_compra(self):
        return self.__pedido_compra

    @pedido_compra.setter
    def pedido_compra(self, pedido_compra):
        self.__pedido_compra = pedido_compra

    @property
    def usuarios(self):
        return self.__usuarios

    @usuarios.setter
    def usuarios(self, usuarios):
        self.__usuarios = usuarios

    @property
    def estoques(self):
        return self.__estoques

    @estoques.setter
    def estoques(self, estoques):
        self.__estoques = estoques

    def json(self):
        return {
            "nome": self.__nome,
            "endereco": self.__endereco,
            "bairro": self.__bairro,
            "cidade": self.__cidade,
            "estado": self.__estado,
            "telefone": self.__telefone,
            "email": self.__email,
            "responsavel": self.__responsavel,
            "whatsapp": self.__whatsapp,
            "cnpj": self.__cnpj,
            "status": self.__status,
            "filiais": self.__filiais,
            "cadastrado_em": self.__cadastrado_em,
            "atualizado_em": self.__atualizado_em,
            "receitas": self.__receitas,
            "pedidosprod": self.__pedidosprod,
            "pedido_compra": self.__pedido_compra,
            "usuarios": self.__usuarios,
            "estoques": self.__estoques

        }

    def query(self):
        return {
            "nome": self.__nome,
            "endereco": self.__endereco,
            "bairro": self.__bairro,
            "cidade": self.__cidade,
            "estado": self.__estado,
            "telefone": self.__telefone,
            "email": self.__email,
            "responsavel": self.__responsavel,
            "whatsapp": self.__whatsapp,
            "cnpj": self.__cnpj,
            "status": self.__status,
            "filiais": self.__filiais,
            "cadastrado_em": self.__cadastrado_em,
            "atualizado_em": self.__atualizado_em,
            "receitas": self.__receitas,
            "pedidosprod": self.__pedidosprod,
            "pedido_compra": self.__pedido_compra,
            "usuarios": self.__usuarios,
            "estoques": self.__estoques

        }
