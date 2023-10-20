
class Produto:
    def __init__(self, nome, descricao, quantidade, compra_unid, peso_pcte, valor, custo_ultima_compra, whatsapp, qrcode, status,
                 estoque_minimo, obs, cadastrado_em, atualizado_em, fornecedor, estoques_produto, mixproduto, pedidos, receitas, reposicoes):

        self.__nome = nome
        self.__descricao = descricao
        self.__quantidade = quantidade
        self.__compra_unid = compra_unid
        self.__peso_pcte = peso_pcte
        self.__valor = valor
        self.__custo_ultima_compra = custo_ultima_compra
        self.__whatsapp = whatsapp
        self.__qrcode = qrcode
        self.__status = status
        self.__estoque_minimo = estoque_minimo
        self.__obs = obs
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__fornecedor = fornecedor
        self.__estoques_produto = estoques_produto
        self.__mixproduto = mixproduto
        self.__pedidos = pedidos
        self.__receitas = receitas
        self.__reposicoes = reposicoes

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
    def whatsapp(self):
        return self.__whatsapp

    @whatsapp.setter
    def whatsapp(self, whatsapp):
        self.__whatsapp = whatsapp

    @property
    def qrcode(self):
        return self.__qrcode

    @qrcode.setter
    def qrcode(self, qrcode):
        self.__qrcode = qrcode

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def estoque_minimo(self):
        return self.__estoque_minimo

    @estoque_minimo.setter
    def estoque_minimo(self, estoque_minimo):
        self.__estoque_minimo = estoque_minimo

    @property
    def obs(self):
        return self.__obs

    @obs.setter
    def obs(self, obs):
        self.__obs = obs

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
    def fornecedor(self):
        return self.__fornecedor

    @fornecedor.setter
    def fornecedor(self, fornecedor):
        self.__fornecedor = fornecedor

    @property
    def estoques_produto(self):
        return self.__estoques_produto

    @estoques_produto.setter
    def estoques_produto(self, estoques_produto):
        self.__estoques_produto = estoques_produto

    @property
    def mixproduto(self):
        return self.__mixproduto

    @mixproduto.setter
    def mixproduto(self, mixproduto):
        self.__mixproduto = mixproduto

    @property
    def pedidos(self):
        return self.__pedidos

    @pedidos.setter
    def pedidos(self, pedidos):
        self.__pedidos = pedidos

    @property
    def receitas(self):
        return self.__receitas

    @receitas.setter
    def receitas(self, receitas):
        self.__receitas = receitas

    @property
    def reposicoes(self):
        return self.__reposicoes

    @reposicoes.setter
    def reposicoes(self, reposicoes):
        self.__reposicoes = reposicoes


