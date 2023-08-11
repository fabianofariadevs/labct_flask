class Estoque:
    def __init__(self, produto_id, cliente_id, nome, preco, validade, valor_ultima_compra, quantidade_op, quantidade_minima, obs):
        self.produto_id = produto_id
        self.cliente_id = cliente_id
        self.nome = nome
        self.preco = preco
        self.validade = validade
        self.valor_ultima_compra = valor_ultima_compra
        self.quantidade_op = quantidade_op
        self.quantidade_minima = quantidade_minima
        self.obs = obs

