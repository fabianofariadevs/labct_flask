
class MixProduto:
    def __init__(self, cod_prod_mix, status, situacao, quantidade, cadastrado_em, atualizado_em,
                 receita, pedidosprod, producoes, produtos):
        self.__cod_prod_mix = cod_prod_mix
        self.__status = status
        self.__situacao = situacao
        self.__quantidade = quantidade
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__receita = receita
       # self.__filiais = filiais
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

class QuantidadeMixProdutos:
    def __init__(self, quantidade, mix_produtos, produto):
        self.__quantidade = quantidade
        self.__mix_produtos = mix_produtos
        self.__produto = produto

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade

    @property
    def mix_produtos(self):
        return self.__mix_produtos

    @mix_produtos.setter
    def mix_produtos(self, mix_produtos):
        self.__mix_produtos = mix_produtos

    @property
    def produto(self):
        return self.__produto

    @produto.setter
    def produto(self, produto):
        self.__produto = produto


class Producao:
    def __init__(self, data_producao, qtde_produzida, status, obs, qr_code, cadastrado_em, atualizado_em,
                 mixprodutos, filial, usuario, pedidosprod):
        self.__data_producao = data_producao
        self.__qtde_produzida = qtde_produzida
        self.__status = status
        self.__obs = obs
        self.__qr_code = qr_code
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__mixprodutos = mixprodutos
        self.__filial = filial
        self.__usuario = usuario
        self.__pedidosprod = pedidosprod

    @property
    def data_producao(self):
        return self.__data_producao

    @data_producao.setter
    def data_producao(self, data_producao):
        self.__data_producao = data_producao

    @property
    def qtde_produzida(self):
        return self.__qtde_produzida

    @qtde_produzida.setter
    def qtde_produzida(self, qtde_produzida):
        self.__qtde_produzida = qtde_produzida

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
    def qr_code(self):
        return self.__qr_code

    @qr_code.setter
    def qr_code(self, qr_code):
        self.__qr_code = qr_code

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
    def mixprodutos(self):
        return self.__mixprodutos

    @mixprodutos.setter
    def mixprodutos(self, mixprodutos):
        self.__mixprodutos = mixprodutos

    @property
    def filial(self):
        return self.__filial

    @filial.setter
    def filial(self, filial):
        self.__filial = filial

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario):
        self.__usuario = usuario

    @property
    def pedidosprod(self):
        return self.__pedidosprod

    @pedidosprod.setter
    def pedidosprod(self, pedidosprod):
        self.__pedidosprod = pedidosprod
