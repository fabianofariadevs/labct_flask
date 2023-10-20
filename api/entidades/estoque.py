class Estoque:
    def __init__(self, produto_id, cliente_id, filial_pdv, nome, preco, validade, valor_ultima_compra, quantidade_op, quantidade_minima, obs, quantidade_atual, status, cadastrado_em, atualizado_em):

        self.produto_id = produto_id
        self.cliente_id = cliente_id
        self.filial_pdv = filial_pdv
        self.nome = nome
        self.preco = preco
        self.validade = validade
        self.valor_ultima_compra = valor_ultima_compra
        self.quantidade_op = quantidade_op
        self.quantidade_minima = quantidade_minima
        self.obs = obs
        self.quantidade_atual = quantidade_atual
        self.status = status
        self.cadastrado_em = cadastrado_em
        self.atualizado_em = atualizado_em

    @property
    def produto_id(self):
        return self.__produto_id

    @produto_id.setter
    def produto_id(self, produto_id):
        self.__produto_id = produto_id

    @property
    def cliente_id(self):
        return self.__cliente_id

    @cliente_id.setter
    def cliente_id(self, cliente_id):
        self.__cliente_id = cliente_id

    @property
    def filial_pdv(self):
        return self.__filial_pdv

    @filial_pdv.setter
    def filial_pdv(self, filial_pdv):
        self.__filial_pdv = filial_pdv

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, preco):
        self.__preco = preco

    @property
    def validade(self):
        return self.__validade

    @validade.setter
    def validade(self, validade):
        self.__validade = validade

    @property
    def valor_ultima_compra(self):
        return self.__valor_ultima_compra

    @valor_ultima_compra.setter
    def valor_ultima_compra(self, valor_ultima_compra):
        self.__valor_ultima_compra = valor_ultima_compra

    @property
    def quantidade_op(self):
        return self.__quantidade_op

    @quantidade_op.setter
    def quantidade_op(self, quantidade_op):
        self.__quantidade_op = quantidade_op

    @property
    def quantidade_minima(self):
        return self.__quantidade_minima

    @quantidade_minima.setter
    def quantidade_minima(self, quantidade_minima):
        self.__quantidade_minima = quantidade_minima

    @property
    def obs(self):
        return self.__obs

    @obs.setter
    def obs(self, obs):
        self.__obs = obs

    @property
    def quantidade_atual(self):
        return self.__quantidade_atual

    @quantidade_atual.setter
    def quantidade_atual(self, quantidade_atual):
        self.__quantidade_atual = quantidade_atual

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


class ReposicaoEstoque:
    def __init__(self, produto_id, data_solicitacao, produto):

        self.produto_id = produto_id
        self.data_solicitacao = data_solicitacao
        self.produto = produto

    @property
    def produto_id(self):
        return self.__produto_id

    @produto_id.setter
    def produto_id(self, produto_id):
        self.__produto_id = produto_id

    @property
    def data_solicitacao(self):
        return self.__data_solicitacao

    @data_solicitacao.setter
    def data_solicitacao(self, data_solicitacao):
        self.__data_solicitacao = data_solicitacao

    @property
    def produto(self):
        return self.__produto

    @produto.setter
    def produto(self, produto):
        self.__produto = produto

