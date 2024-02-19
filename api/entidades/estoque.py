class Estoque:
    def __init__(self, produto, fornecedor, cliente, filiais, nome, validade, valor_ultima_compra, quantidade_minima, obs,
                 quantidade_atual, status, cadastrado_em, atualizado_em):

        self.produto = produto
        self.fornecedor = fornecedor
        self.cliente = cliente
        self.filiais = filiais
        self.nome = nome
        self.validade = validade
        self.valor_ultima_compra = valor_ultima_compra
        self.quantidade_minima = quantidade_minima
        self.obs = obs
        self.quantidade_atual = quantidade_atual
        self.status = status
        self.cadastrado_em = cadastrado_em
        self.atualizado_em = atualizado_em

    @property
    def produtos(self):
        return self.__produtos

    @produtos.setter
    def produtos(self, produtos):
        self.__produtos = produtos

    @property
    def fornecedor(self):
        return self.__fornecedor

    @fornecedor.setter
    def fornecedor(self, fornecedor):
        self.__fornecedor = fornecedor

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente

    @property
    def filiais(self):
        return self.__filiais

    @filiais.setter
    def filiais(self, filiais):
        self.__filiais = filiais

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

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

