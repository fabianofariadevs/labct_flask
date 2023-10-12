class Filial:
    def __int__(self, nome, endereco, bairro, cidade, estado, whatsapp, responsavel, cnpj, status,
                cadastrado_em, atualizado_em, clientes, mixprodutos, pedidosprod):
        self.__nome = nome
        self.__endereco = endereco
        self.__bairro = bairro
        self.__cidade = cidade
        self.__estado = estado
        self.__whatsapp = whatsapp
        self.__responsavel = responsavel
        self.__cnpj = cnpj
        self.__status = status
        self.__cadastrado_em = cadastrado_em
        self.__atualizado_em = atualizado_em
        self.__clientes = clientes
        self.__mixprodutos = mixprodutos
        self.__pedidosprod = pedidosprod

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco

    @property
    def bairro(self):
        return self.__bairro

    @bairro.setter
    def bairro(self, bairro):
        self.__bairro = bairro

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        self.__estado = estado

    @property
    def responsavel(self):
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel):
        self.__responsavel = responsavel

    @property
    def whatsapp(self):
        return self.__whatsapp

    @whatsapp.setter
    def whatsapp(self, whatsapp):
        self.__whatsapp = whatsapp

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        self.__cnpj = cnpj

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
    def pedidosprod(self):
        return self.__pedidosprod

    @pedidosprod.setter
    def pedidosprod(self, pedidosprod):
        self.__pedidosprod = pedidosprod

    def json(self):
        return {
            "nome": self.__nome,
            "endereco": self.__endereco,
            "bairro": self.__bairro,
            "cidade": self.__cidade,
            "estado": self.__estado,
            "whatsapp": self.__whatsapp,
            "responsavel": self.__responsavel,
            "cnpj": self.__cnpj,
            "status": self.__status,
            "cadastrado_em": self.__cadastrado_em,
            "atualizado_em": self.__atualizado_em,
            "cliente": self.__cliente,
            "mixprodutos": self.__mixprodutos,
            "pedidosprod": self.__pedidosprod
        }

