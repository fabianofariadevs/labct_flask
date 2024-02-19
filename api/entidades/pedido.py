#TODO pedido COMPRA=1(entrada"+") e pedido de produção=2(saida"-")
#TODO CLASSE PARA ENTIDADES PEDIDO E PEDIDOPRODUCAO

class Pedido:
    def __init__(self, qtde_pedido, data_pedido, data_entrega, status, obs, cadastrado_em, atualizado_em,
                 produtos, clientes, fornecedores):
        self.__qtde_pedido = qtde_pedido
        self.__data_pedido = data_pedido
        self.__data_entrega = data_entrega
        self.__status = status
        self.__obs = obs
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__produtos = produtos
        self.__clientes = clientes
        self.__fornecedores = fornecedores

    @property
    def qtde_pedido(self):
        return self.__qtde_pedido

    @qtde_pedido.setter
    def qtde_pedido(self, qtde_pedido):
        self.__qtde_pedido = qtde_pedido

    @property
    def data_pedido(self):
        return self.__data_pedido

    @data_pedido.setter
    def data_pedido(self, data_pedido):
        self.__data_pedido = data_pedido

    @property
    def data_entrega(self):
        return self.__data_entrega

    @data_entrega.setter
    def data_entrega(self, data_entrega):
        self.__data_entrega = data_entrega

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

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
    def produtos(self):
        return self.__produtos

    @produtos.setter
    def produtos(self, produtos):
        self.__produtos = produtos

    @property
    def clientes(self):
        return self.__clientes

    @clientes.setter
    def clientes(self, clientes):
        self.__clientes = clientes

    @property
    def fornecedores(self):
        return self.__fornecedores

    @fornecedores.setter
    def fornecedores(self, fornecedores):
        self.__fornecedores = fornecedores


class PedidoProducao:
    def __init__(self, data_pedido, data_entrega, qtde_pedido, situacao, status, obs, cadastrado_em, atualizado_em,
                 filiais, cliente, mixprodutos, producoes):

        self.__data_pedido = data_pedido
        self.__data_entrega = data_entrega
        self.__qtde_pedido = qtde_pedido
        self.__situacao = situacao
        self.__status = status
        self.__obs = obs
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__filiais = filiais
        self.__cliente = cliente
        self.__mixprodutos = mixprodutos
        self.__producoes = producoes

    @property
    def data_pedido(self):
        return self.__data_pedido

    @data_pedido.setter
    def data_pedido(self, data_pedido):
        self.__data_pedido = data_pedido

    @property
    def data_entrega(self):
        return self.__data_entrega

    @data_entrega.setter
    def data_entrega(self, data_entrega):
        self.__data_entrega = data_entrega

    @property
    def situacao(self):
        return self.__situacao

    @situacao.setter
    def situacao(self, situacao):
        self.__situacao = situacao

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def qtde_pedido(self):
        return self.__qtde_pedido

    @qtde_pedido.setter
    def qtde_pedido(self, qtde_pedido):
        self.__qtde_pedido = qtde_pedido

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
    def filiais(self):
        return self.__filiais

    @filiais.setter
    def filiais(self, filiais):
        self.__filiais = filiais

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente):
        self.__cliente = cliente

    @property
    def mixprodutos(self):
        return self.__mixprodutos

    @mixprodutos.setter
    def mixprodutos(self, mixprodutos):
        self.__mixprodutos = mixprodutos

    @property
    def producoes(self):
        return self.__producoes

    @producoes.setter
    def producoes(self, producoes):
        self.__producoes = producoes

