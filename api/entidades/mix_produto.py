
class Mixproduto:
    def __init__(self, cod_prod_mix, status, situacao, quantidade, cadastrado_em, atualizado_em, receita, filiais, pedidosprod, producoes, produtos):
        self.__cod_prod_mix = cod_prod_mix
        self.__status = status
        self.__situacao = situacao
        self.__quantidade = quantidade
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__receita = receita
        self.__filiais = filiais
        self.__pedidosprod = pedidosprod
        self.__producoes = producoes
        self.__produtos = produtos

    @property
    def cod_prod_mix(self):
        return self.__cod_prod_mix

    @cod_prod_mix.setter
    def cod_prod_mix(self, cod_prod_mix):
        self.__cod_prod_mix = cod_prod_mix

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def situacao(self):
        return self.__situacao

    @situacao.setter
    def situacao(self, situacao):
        self.__situacao = situacao

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade

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
    def receita(self):
        return self.__receita

    @receita.setter
    def receita(self, receita):
        self.__receita = receita

    @property
    def filiais(self):
        return self.__filiais

    @filiais.setter
    def filiais(self, filiais):
        self.__filiais = filiais

    @property
    def pedidosprod(self):
        return self.__pedidosprod

    @pedidosprod.setter
    def pedidosprod(self, pedidosprod):
        self.__pedidosprod = pedidosprod

    @property
    def producoes(self):
        return self.__producoes

    @producoes.setter
    def producoes(self, producoes):
        self.__producoes = producoes

    @property
    def produtos(self):
        return self.__produtos

    @produtos.setter
    def produtos(self, produtos):
        self.__produtos = produtos

    def to_dict(self):
        return {
            "cod_prod_mix": self.cod_prod_mix,
            "status": self.status,
            "situacao": self.situacao,
            "quantidade": self.quantidade,
            "cadastrado_em": self.cadastrado_em,
            "atualizado_em": self.atualizado_em,
            "receita": self.receita,
            "filiais": self.filiais,
            "pedidosprod": self.pedidosprod,
            "producoes": self.producoes,
            "produtos": self.produtos
        }

