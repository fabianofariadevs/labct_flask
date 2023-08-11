
class Produto:
    def __init__(self, nome, descricao, quantidade, fornecedor_id, cliente_id, compra_unid, peso_pcte, valor, custo_ultima_compra, status, cadastrado_em, atualizado_em):
        self.__nome = nome
        self.__descricao = descricao
        self.__quantidade = quantidade
        self.__fornecedor_id = fornecedor_id
        self.__cliente_id = cliente_id
        self.__compra_unid = compra_unid
        self.__peso_pcte = peso_pcte
        self.__valor = valor
        self.__custo_ultima_compra = custo_ultima_compra
        self.__status = status
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade

    @property
    def cliente_id(self):
        return self.__cliente_id

    @cliente_id.setter
    def cliente_id(self, cliente_id):
        self.__cliente_id = cliente_id

    @property
    def fornecedor_id(self):
        return self.__fornecedor_id

    @fornecedor_id.setter
    def fornecedor_id(self, fornecedor_id):
        self.__fornecedor_id = fornecedor_id

    @property
    def compra_unid(self):
        return self.__compra_unid

    @compra_unid.setter
    def compra_unid(self, compra_unid):
        self.__compra_unid = compra_unid

    @property
    def peso_pcte(self):
        return self.__peso_pcte

    @peso_pcte.setter
    def peso_pcte(self, peso_pcte):
        self.__peso_pcte = peso_pcte

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        self.__valor = valor

    @property
    def custo_ultima_compra(self):
        return self.__custo_ultima_compra

    @custo_ultima_compra.setter
    def custo_ultima_compra(self, custo_ultima_compra):
        self.__custo_ultima_compra = custo_ultima_compra

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