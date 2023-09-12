
class Receita:
    def __init__(self, descricao_mix, modo_preparo, departamento, rend_kg, rend_unid, validade, status, cadastrado_em, atualizado_em,
                 produto_id, quantidades, filiais, produtos, pedidosprod):
        self.__descricao_mix = descricao_mix
        self.__modo_preparo = modo_preparo
        self.__departamento = departamento
        self.__rend_kg = rend_kg
        self.__rend_unid = rend_unid
        self.__validade = validade
        self.__status = status
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__produtos_id = produto_id
        self.__quantidades = quantidades
        self.__filiais = filiais
        self.__produtos = produtos
        self.__pedidosprod = pedidosprod

    @property
    def descricao_mix(self):
        return self.__descricao_mix

    @descricao_mix.setter
    def descricao_mix(self, descricao_mix):
        self.__descricao_mix = descricao_mix

    @property
    def modo_preparo(self):
        return self.__modo_preparo

    @modo_preparo.setter
    def modo_preparo(self, modo_preparo):
        self.__modo_preparo = modo_preparo

    @property
    def departamento(self):
        return self.__departamento

    @departamento.setter
    def departamento(self, departamento):
        self.__departamento = departamento

    @property
    def rend_kg(self):
        return self.__rend_kg

    @rend_kg.setter
    def rend_kg(self, rend_kg):
        self.__rend_kg = rend_kg

    @property
    def rend_unid(self):
        return self.__rend_unid

    @rend_unid.setter
    def rend_unid(self, rend_unid):
        self.__rend_unid = rend_unid

    @property
    def validade(self):
        return self.__validade

    @validade.setter
    def validade(self, validade):
        self.__validade = validade

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
    def produto_id(self):
        return self.__produtos_id

    @produto_id.setter
    def produto_id(self, produto_id):
        self.__produtos_id = produto_id

    @property
    def quantidades(self):
        return self.__quantidades

    @quantidades.setter
    def quantidades(self, quantidades):
        self.__quantidades = quantidades

    @property
    def filiais(self):
        return self.__filiais

    @filiais.setter
    def filiais(self, filiais):
        self.__filiais = filiais

    @property
    def produtos(self):
        return self.__produtos

    @produtos.setter
    def produtos(self, produtos):
        self.__produtos = produtos

    @property
    def pedidosprod(self):
        return self.__pedidosprod

    @pedidosprod.setter
    def pedidosprod(self, pedidosprod):
        self.__pedidosprod = pedidosprod

    def json(self):
        return {
            "descricao_mix": self.__descricao_mix,
            "modo_preparo": self.__modo_preparo,
            "departamento": self.__departamento,
            "rend_kg": self.__rend_kg,
            "rend_unid": self.__rend_unid,
            "validade": self.__validade,
            "status": self.__status,
            "cadastrado_em": self.__cadastrado_em,
            "atualizado_em": self.__atualizado_em,
            "produto_id": self.__produtos_id,
            "quantidades": self.__quantidades,
            "filiais": self.__filiais,
            "produtos": self.__produtos,
            "pedidosprod": self.__pedidosprod
        }

