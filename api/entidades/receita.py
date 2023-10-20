
class Receita:
    def __init__(self, descricao_mix, modo_preparo, departamento, rend_kg, rend_unid, validade, status, cadastrado_em, atualizado_em,
                 filiais, clientes, ingredientes, pedidosprod, usuario):

        self.__descricao_mix = descricao_mix
        self.__modo_preparo = modo_preparo
        self.__departamento = departamento
        self.__rend_kg = rend_kg
        self.__rend_unid = rend_unid
        self.__validade = validade
        self.__status = status
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__filiais = filiais
        self.__clientes = clientes
        self.__ingredientes = ingredientes
        self.__pedidosprod = pedidosprod
        self.__usuario = usuario

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
    def filiais(self):
        return self.__filiais

    @filiais.setter
    def filiais(self, filiais):
        self.__filiais = filiais

    @property
    def clientes(self):
        return self.__clientes

    @clientes.setter
    def clientes(self, clientes):
        self.__clientes = clientes

    @property
    def ingredientes(self):
        return self.__ingredientes

    @ingredientes.setter
    def ingredientes(self, ingredientes):
        self.__ingredientes = ingredientes

    @property
    def pedidosprod(self):
        return self.__pedidosprod

    @pedidosprod.setter
    def pedidosprod(self, pedidosprod):
        self.__pedidosprod = pedidosprod

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario):
        self.__usuario = usuario

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
            "quantidades": self.__quantidades,
            "filiais": self.__filiais,
            "clientes": self.__clientes,
            "ingredientes": self.ingredientes,
            "pedidosprod": self.__pedidosprod,
            "usuario": self.__usuario
        }

class Ingredientes:
    def __init__(self, nome, quantidade, unidade, receita_id, receita):

        self.__nome = nome
        self.__quantidade = quantidade
        self.__unidade = unidade
        self.__receita_id = receita_id
        self.__receita = receita

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade

    @property
    def unidade(self):
        return self.__unidade

    @unidade.setter
    def unidade(self, unidade):
        self.__unidade = unidade

    @property
    def receita_id(self):
        return self.__receita_id

    @receita_id.setter
    def receita_id(self, receita_id):
        self.__receita_id = receita_id

    @property
    def receita(self):
        return self.__receita

    @receita.setter
    def receita(self, receita):
        self.__receita = receita

    def json(self):
        return {
            "nome": self.__nome,
            "quantidade": self.__quantidade,
            "unidade": self.__unidade,
            "receita_id": self.__receita_id,
            "receita": self.__receita
        }