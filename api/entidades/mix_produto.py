
class Mixproduto:
    def __init__(self, cod_prod_mix, status, cadastrado_em, atualizado_em, receita_id, filial_id, cliente_id):
        self.__cod_prod_mix = cod_prod_mix
        self.__status = status
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__receita_id = receita_id
        self.__filial_id = filial_id
        self.__cliente_id = cliente_id

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
    def receita_id(self):
        return self.__receita_id

    @receita_id.setter
    def receita_id(self, receita_id):
        self.__receita_id = receita_id

    @property
    def filial_id(self):
        return self.__filial_id

    @filial_id.setter
    def filial_id(self, filial_id):
        self.__filial_id = filial_id

    @property
    def cliente_id(self):
        return self.__cliente_id

    @cliente_id.setter
    def cliente_id(self, cliente_id):
        self.__cliente_id = cliente_id

    def json(self):
        return {
            "cod_prod_mix": self.__cod_prod_mix,
            "status": self.__status,
            "cadastrado_em": self.__cadastrado_em,
            "atualizado_em": self.__atualizado_em,
            "receita_id": self.__receita_id,
            "filial_id": self.__filial_id,
            "cliente_id": self.__cliente_id
        }


