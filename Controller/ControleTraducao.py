from model.Traducao import Traducao
from model.Token import Token
from model.Carteira import Carteira
from datetime import datetime


def gerarTokens(energiaGerada, cliente_id, data_expedicao=None, carteira=None):
    
    # Usar data atual se não fornecida
    if data_expedicao is None:
        data_expedicao = datetime.now().strftime("%Y-%m-%d")
    
    # Criar carteira vazia se não fornecida
    if carteira is None:
        carteira = Carteira(
            codigo=f"CART_{cliente_id}",
            senha="",
            cliente=None,
            tokens=[]
        )
    
    # Criar objeto Traducao e calcular tokens
    traducao = Traducao(energiaGerada, cliente_id)
    tokens_quantidade = traducao.calcularTokensGerados()
    
    # Gerar objetos Token e adicionar à carteira
    tokens_criados = []
    for i in range(tokens_quantidade):
        token = Token(id=i+1, dataExpedicao=data_expedicao)
        tokens_criados.append(token)
        carteira.tokens.append(token)
    
    # Retornar resultado detalhado
    return {
        'tokens_quantidade': tokens_quantidade,
        'tokens': tokens_criados,
        'carteira': carteira
    }
