from model.Cliente import Cliente
from model.Carteira import Carteira
from model.Token import Token
from model.Produto import Produto
from model.Item import Item
from model.Troca import Troca
from model.EnergiaGerada import EnergiGerada
from model.Traducao import Traducao
from Controller.ControleTraducao import gerarTokens
from Controller.ControleTroca import calcular_valor_total, calcular_tokens_necessarios, realizar_troca


def separador(titulo):
    """Função auxiliar para criar separadores visuais"""
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}\n")


def exemplo_cliente():
    """Exemplo 1: Criar e usar a classe Cliente"""
    separador("EXEMPLO 1: CLASSE CLIENTE")
    
    cliente1 = Cliente(
        nome="João Silva",
        telefone="11999887766",
        email="joao@email.com",
        id=1,
        cpf="12345678900",
        endereco="Rua A, 123"
    )
    
    print(f"Nome: {cliente1.getNome()}")
    print(f"Email: {cliente1.getEmail()}")
    print(f"Telefone: {cliente1.getTelefone()}")
    print(f"CPF: {cliente1.getCpf()}")
    print(f"Endereço: {cliente1.getEndereco()}")
    print(f"ID: {cliente1.getId()}")


def exemplo_produto_e_item():
    """Exemplo 2: Produtos e Itens"""
    separador("EXEMPLO 2: PRODUTOS E ITENS")
    
    produto1 = Produto(
        nome="Painel Solar",
        preco=1500.00,
        descricao="Painel solar de 400W"
    )
    
    produto2 = Produto(
        nome="Inversor",
        preco=2000.00,
        descricao="Inversor solar 5kW"
    )
    
    print("Produtos disponíveis:")
    print(f"1. {produto1.getNome()} - R$ {produto1.getPreco()}")
    print(f"   Descrição: {produto1.getDescricao()}")
    print(f"\n2. {produto2.getNome()} - R$ {produto2.getPreco()}")
    print(f"   Descrição: {produto2.getDescricao()}")
    
    item1 = Item(quantidade=2, produto=produto1)
    item2 = Item(quantidade=1, produto=produto2)
    
    print(f"\nItens no carrinho:")
    print(f"- {item1.getQuantidade()}x {item1.getProduto().getNome()} = R$ {item1.getSubValor()}")
    print(f"- {item2.getQuantidade()}x {item2.getProduto().getNome()} = R$ {item2.getSubValor()}")


def exemplo_troca():
    """Exemplo 3: Transação de Troca"""
    separador("EXEMPLO 3: TRANSAÇÃO DE TROCA")

    cliente = Cliente(
        nome="Maria Santos",
        telefone="11988776655",
        email="maria@email.com",
        id=2,
        cpf="98765432100",
        endereco="Rua B, 456"
    )

    produto = Produto(
        nome="Bateria Solar",
        preco=3000.00,
        descricao="Bateria LiFePO4 10kWh"
    )

    item = Item(quantidade=1, produto=produto)

    troca = Troca(
        id=101,
        data="2024-06-11",
        cliente=cliente,
        item=[item]
    )
    
    print(f"ID da Troca: {troca.getId()}")
    print(f"Data: {troca.getData()}")
    print(f"Cliente: {troca.getCliente().getNome()}")
    print(f"Item(ns): {len(troca.getItem())} produto(s)")
    print(f"Valor Total: R$ {troca.getValorTotal():.2f}")


def exemplo_token():
    """Exemplo 4: Tokens e Carteira"""
    separador("EXEMPLO 4: TOKENS E CARTEIRA")

    tokens = []
    for i in range(1, 6):
        token = Token(id=i, dataExpedicao="2024-06-11")
        tokens.append(token)
        print(f"Token {token.getId()} - Data de Expedição: {token.getDataExpedicao()}")

    cliente = Cliente(
        nome="Pedro Costa",
        telefone="11987654321",
        email="pedro@email.com",
        id=3,
        cpf="55555555555",
        endereco="Rua C, 789"
    )
    
    carteira = Carteira(
        codigo="CART001",
        senha="senha123",
        cliente=cliente,
        tokens=tokens
    )
    
    print(f"\nCarteira criada:")
    print(f"Código: {carteira.getCodigo()}")
    print(f"Titular: {carteira.getCliente().getNome()}")
    print(f"Total de Tokens: {carteira.totalTokens()}")


def exemplo_energia_gerada():
    """Exemplo 5: Energia Gerada"""
    separador("EXEMPLO 5: ENERGIA GERADA")
    
    cliente = Cliente(
        nome="Ana Silva",
        telefone="11912345678",
        email="ana@email.com",
        id=4,
        cpf="11111111111",
        endereco="Rua D, 101"
    )
    
    energia = EnergiGerada(
        quantidade=500,  
        periodo="Junho/2024",
        cliente=cliente
    )
    
    print(f"Cliente: {energia.getCliente().getNome()}")
    print(f"Quantidade gerada: {energia.getQuantidade()} kWh")
    print(f"Período: {energia.getPeriodo()}")


def exemplo_traducao():
    """Exemplo 6: Tradução de Energia para Tokens"""
    separador("EXEMPLO 6: TRADUÇÃO (ENERGIA → TOKENS)")
    
    print("Testando a função calcularTokensGerados:")
    print("\nCálculo: tokens = int(energia * 0.1)\n")

    energias = [10, 50, 100, 255, 1000]
    
    for energia in energias:
        traducao = Traducao(energiaGerada=energia, id=1)
        tokens = traducao.calcularTokensGerados()
        print(f"Energia: {energia} kWh → Tokens gerados: {tokens} (tipo: {type(tokens).__name__})")


def exemplo_fluxo_troca():
    """Exemplo 7: Fluxo completo de troca usando tokens gerados"""
    separador("EXEMPLO 7: FLUXO COMPLETO DE TROCA")

    cliente = Cliente(
        nome="Lucas Ferreira",
        telefone="11944443333",
        email="lucas@email.com",
        id=6,
        cpf="22233344455",
        endereco="Rua F, 303"
    )

    energia_gerada = 120
    print("1️⃣ Calcular tokens a partir da energia gerada")
    traducao = Traducao(energiaGerada=energia_gerada, id=cliente.getId())
    tokens_gerados = traducao.calcularTokensGerados()
    print(f"   Energia: {energia_gerada} kWh → Tokens gerados: {tokens_gerados}")

    carteira = Carteira(
        codigo="CART_LUCAS_006",
        senha="senha456",
        cliente=cliente,
        tokens=[]
    )

    print("2️⃣ Adicionar tokens à carteira usando o controlador")
    resultado_tokens = gerarTokens(
        energiaGerada=energia_gerada,
        cliente_id=cliente.getId(),
        data_expedicao="2024-06-11",
        carteira=carteira
    )
    carteira = resultado_tokens['carteira']
    print(f"   Carteira {carteira.getCodigo()} criada com {carteira.totalTokens()} tokens")

    produto_a = Produto(nome="Kit Solar Compacto", preco=40.0, descricao="Kit com 2 painéis e cabos")
    produto_b = Produto(nome="Bateria Portátil", preco=60.0, descricao="Bateria para armazenamento small")
    item_a = Item(quantidade=1, produto=produto_a)
    item_b = Item(quantidade=1, produto=produto_b)

    print("3️⃣ Realizar troca de tokens por itens")
    resultado_troca = realizar_troca(
        carteira=carteira,
        itens=[item_a, item_b],
        data="2024-06-11",
        id_troca=601,
        valor_por_token=10
    )

    print(f"   Valor total da compra: R$ {resultado_troca['valor_total']}")
    print(f"   Tokens gastos: {resultado_troca['tokens_gastos']}")
    print(f"   Tokens restantes: {resultado_troca['tokens_restantes']}")

    troca = resultado_troca['troca']
    print("4️⃣ Resumo da troca")
    print(f"   Troca ID: {troca.getId()}")
    print(f"   Cliente: {troca.getCliente().getNome()}")
    print(f"   Data: {troca.getData()}")
    print(f"   Itens na troca: {len(troca.getItem())}")
    print(f"   Tokens finais na carteira: {resultado_troca['carteira'].totalTokens()}")


def exemplo_completo():
    """Exemplo 8: Fluxo completo do sistema"""
    separador("EXEMPLO 8: FLUXO COMPLETO DO SISTEMA")
    
    print("Simulando um fluxo completo:\n")
    
    print("1️⃣ Criando cliente...")
    cliente = Cliente(
        nome="Carlos Oliveira",
        telefone="11911111111",
        email="carlos@email.com",
        id=5,
        cpf="77777777777",
        endereco="Rua E, 202"
    )
    print(f"   Cliente criado: {cliente.getNome()}\n")

    print("2️⃣ Registrando energia gerada...")
    energia_gerada = 750  # kWh
    energia = EnergiGerada(
        quantidade=energia_gerada,
        periodo="Junho/2024",
        cliente=cliente
    )
    print(f"   Energia registrada: {energia.getQuantidade()} kWh no período {energia.getPeriodo()}\n")

    print("3️⃣ Calculando tokens a gerar...")
    traducao = Traducao(energiaGerada=energia_gerada, id=1)
    tokens_quantidade = traducao.calcularTokensGerados()
    print(f"   Tokens gerados: {tokens_quantidade}\n")

    print("4️⃣ Criando carteira com tokens...")
    carteira = Carteira(
        codigo="CART_CARLOS_001",
        senha="senha_segura_123",
        cliente=cliente,
        tokens=[]
    )
    resultado_tokens = gerarTokens(
        energiaGerada=energia_gerada,
        cliente_id=cliente.getId(),
        data_expedicao="2024-06-11",
        carteira=carteira
    )
    carteira = resultado_tokens['carteira']
    tokens_quantidade = resultado_tokens['tokens_quantidade']
    print(f"   Carteira criada com {carteira.totalTokens()} tokens\n")

    print("5️⃣ Cliente usa tokens para comprar produtos...")
    produto_disponivel = Produto(
        nome="Placa Solar Premium",
        preco=75.00, 
        descricao="Placa de alta eficiência"
    )
    
    quantidade_comprada = 2
    item = Item(quantidade=quantidade_comprada, produto=produto_disponivel)
    
    troca = Troca(
        id=201,
        data="2024-06-11",
        cliente=cliente,
        item=[item]
    )
    
    print(f"   Produto: {item.getProduto().getNome()}")
    print(f"   Quantidade: {quantidade_comprada}")
    print(f"   Valor por unidade: R$ {item.getProduto().getPreco()}")
    print(f"   Valor total da compra: R$ {troca.getValorTotal()}\n")
  
    print("6️⃣ Resumo da operação:")
    print(f"   - Cliente: {cliente.getNome()}")
    print(f"   - Carteira: {carteira.getCodigo()}")
    print(f"   - Tokens gerados: {carteira.totalTokens()}")
    print(f"   - Compra realizada (ID {troca.getId()}): R$ {troca.getValorTotal()}")


def testar_controle_troca():
    cliente = Cliente(
        nome="Teste Usuario",
        telefone="11900000000",
        email="teste@email.com",
        id=10,
        cpf="00000000000",
        endereco="Rua Teste, 10"
    )

    carteira = Carteira(
        codigo="CART_TESTE",
        senha="senha",
        cliente=cliente,
        tokens=[Token(id=i, dataExpedicao="2024-06-11") for i in range(1, 11)]
    )

    produto1 = Produto(nome="Produto A", preco=50.0, descricao="Produto A desc")
    produto2 = Produto(nome="Produto B", preco=30.0, descricao="Produto B desc")
    item1 = Item(quantidade=1, produto=produto1)
    item2 = Item(quantidade=2, produto=produto2)

    print("\n=== TESTES DO CONTROLE TROCA ===")

    total = calcular_valor_total([item1, item2])
    assert total == 110.0, f"total esperado 110.0, obtido {total}"
    print("✓ calcular_valor_total passou")

    tokens_necessarios = calcular_tokens_necessarios([item1, item2], valor_por_token=25)
    assert tokens_necessarios == 5, f"tokens esperados 5, obtido {tokens_necessarios}"
    print("✓ calcular_tokens_necessarios passou")

    resultado = realizar_troca(
        carteira=Carteira(
            codigo="CART_TESTE",
            senha="senha",
            cliente=cliente,
            tokens=[Token(id=i, dataExpedicao="2024-06-11") for i in range(1, 11)]
        ),
        itens=[item1, item2],
        data="2024-06-11",
        id_troca=500,
        valor_por_token=50
    )
    assert resultado['valor_total'] == 110.0, "valor_total incorreto"
    assert resultado['tokens_gastos'] == 3, "tokens_gastos incorreto"
    assert resultado['tokens_restantes'] == 7, "tokens_restantes incorreto"
    assert resultado['troca'].getId() == 500, "id da troca incorreto"
    assert resultado['troca'].getCliente().getNome() == "Teste Usuario", "cliente incorreto"
    print("✓ realizar_troca sucesso passou")

    try:
        realizar_troca(
            carteira=Carteira(
                codigo="CART_TESTE",
                senha="senha",
                cliente=cliente,
                tokens=[Token(id=i, dataExpedicao="2024-06-11") for i in range(1, 11)]
            ),
            itens=[item1, item2],
            data="2024-06-11",
            id_troca=501,
            valor_por_token=5
        )
        assert False, "esperava ValueError por tokens insuficientes"
    except ValueError:
        print("✓ realizar_troca tokens insuficientes passou")

    print("=== TESTES DO CONTROLE TROCA CONCLUÍDOS ===\n")


def main():
    """Função principal que executa todos os exemplos"""
    print("\n" + "="*60)
    print("  EXEMPLOS PRÁTICOS DO PROJETO - SISTEMA DE TOKENS")
    print("="*60)
    
    try:
        exemplo_cliente()
        exemplo_produto_e_item()
        exemplo_troca()
        exemplo_token()
        exemplo_energia_gerada()
        exemplo_traducao()
        exemplo_fluxo_troca()
        testar_controle_troca()
        exemplo_completo()
        
        separador("CONCLUSÃO")
        print("✓ Todos os exemplos foram executados com sucesso!")
        print("✓ O sistema funciona corretamente com todas as classes integradas.")
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
