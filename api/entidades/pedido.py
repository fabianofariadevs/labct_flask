#TODO pedido COMPRA=1(entrada"+") e pedido de produção=2(saida"-")
#TODO CLASSE PARA ENTIDADES PEDIDO E PEDIDOPRODUCAO

class Pedido:
    def __init__(self, qtde_pedido, data_pedido, data_entrega, status, obs, produto_id, fornecedor_id, filial_pdv, cadastrado_em, atualizado_em):
        self.__qtde_pedido = qtde_pedido
        self.__data_pedido = data_pedido
        self.__data_entrega = data_entrega
        self.__status = status
        self.__obs = obs
        self.__produto_id = produto_id
        self.__fornecedor_id = fornecedor_id
        self.__filial_pdv = filial_pdv
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em

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
    def produto_id(self):
        return self.__produto_id

    @produto_id.setter
    def produto_id(self, produto_id):
        self.__produto_id = produto_id

    @property
    def fornecedor_id(self):
        return self.__fornecedor_id

    @fornecedor_id.setter
    def fornecedor_id(self, fornecedor_id):
        self.__fornecedor_id = fornecedor_id

    @property
    def filial_pdv(self):
        return self.__filial_pdv
    @filial_pdv.setter

    def filial_pdv(self, filial_pdv):
        self.__filial_pdv = filial_pdv

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


class PedidoProducao:
    def __init__(self, data_pedido, data_entrega, qtde_pedido, status, obs, receita_id, filial_pdv, cadastrado_em, atualizado_em):
        self.__data_pedido = data_pedido
        self.__data_entrega = data_entrega
        self.__qtde_pedido = qtde_pedido
        self.__status = status
        self.__obs = obs
        self.__receita_id = receita_id
        self.__filial_pdv = filial_pdv
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em

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
    def receita_id(self):
        return self.__receita_id

    @receita_id.setter
    def receita_id(self, receita_id):
        self.__receita_id = receita_id

    @property
    def filial_pdv(self):
        return self.__filial_pdv

    @filial_pdv.setter
    def filial_pdv(self, filial_pdv):
        self.__filial_pdv = filial_pdv

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