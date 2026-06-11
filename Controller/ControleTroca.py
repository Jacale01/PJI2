import math
from model.Troca import Troca
from model.Item import Item
from model.Carteira import Carteira


def calcular_valor_total(itens):
    """Calcula o valor total de uma lista de itens."""
    return sum(item.getSubValor() for item in itens)


def calcular_tokens_necessarios(itens, valor_por_token=1):
    """Calcula quantos tokens são necessários para pagar os itens."""
    if valor_por_token <= 0:
        raise ValueError("valor_por_token deve ser maior que zero")
    total = calcular_valor_total(itens)
    return math.ceil(total / valor_por_token)


def remover_tokens_da_carteira(carteira, quantidade):
    """Remove uma quantidade de tokens da carteira, se disponível."""
    if quantidade > len(carteira.tokens):
        raise ValueError("Tokens insuficientes na carteira")
    del carteira.tokens[:quantidade]
    return carteira


def realizar_troca(carteira, itens, data, id_troca, valor_por_token=1):
    """Realiza a troca de tokens por itens compostos por produtos."""
    if not isinstance(carteira, Carteira):
        raise TypeError("carteira deve ser um objeto Carteira")
    if not isinstance(itens, list) or not itens:
        raise ValueError("itens deve ser uma lista não vazia de objetos Item")
    for item in itens:
        if not isinstance(item, Item):
            raise TypeError("todos os elementos de itens devem ser objetos Item")

    tokens_necessarios = calcular_tokens_necessarios(itens, valor_por_token=valor_por_token)
    if tokens_necessarios > carteira.totalTokens():
        raise ValueError("Tokens insuficientes para realizar a troca")

    troca = Troca(
        id=id_troca,
        data=data,
        cliente=carteira.getCliente(),
        item=itens
    )

    carteira = remover_tokens_da_carteira(carteira, tokens_necessarios)

    return {
        'troca': troca,
        'tokens_gastos': tokens_necessarios,
        'tokens_restantes': carteira.totalTokens(),
        'carteira': carteira,
        'valor_total': calcular_valor_total(itens)
    }

