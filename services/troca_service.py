from repository.TrocaRepository import TrocaRepository


def _build_cliente(cliente_data):
    if cliente_data is None:
        return None
    return {
        "id": cliente_data.get("id"),
        "nome": cliente_data.get("nome"),
        "telefone": cliente_data.get("telefone"),
        "email": cliente_data.get("email"),
        "cpf": cliente_data.get("cpf"),
        "endereco": cliente_data.get("endereco"),
    }


def _build_itens(itens_data):
    if itens_data is None:
        return []
    itens = []
    for item_data in itens_data:
        produto = item_data.get("produto", {})
        itens.append({
            "quantidade": item_data.get("quantidade", 0),
            "produto": {
                "nome": produto.get("nome"),
                "preco": produto.get("preco", 0),
                "descricao": produto.get("descricao"),
            },
        })
    return itens


def create_troca(cliente, itens, data):
    if cliente is None or itens is None:
        raise ValueError("campos 'cliente' e 'itens' são obrigatórios")
    return TrocaRepository.create(_build_cliente(cliente), _build_itens(itens), data)


def list_trocas():
    return TrocaRepository.list_all()


def get_troca(troca_id):
    return TrocaRepository.find_by_id(troca_id)


def update_troca(troca_id, cliente=None, itens=None, data=None):
    return TrocaRepository.update(
        troca_id,
        cliente=_build_cliente(cliente) if cliente is not None else None,
        itens=_build_itens(itens) if itens is not None else None,
        data=data,
    )


def delete_troca(troca_id):
    return TrocaRepository.delete(troca_id)
