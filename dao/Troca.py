from model.Troca import Troca

_troca_store = []
_next_troca_id = 1


def create(cliente, itens, data):
    global _next_troca_id
    troca = Troca(id=_next_troca_id, data=data, cliente=cliente, item=itens)
    _troca_store.append(troca)
    _next_troca_id += 1
    return troca


def list_all():
    return list(_troca_store)


def find_by_id(troca_id):
    return next((t for t in _troca_store if t.getId() == troca_id), None)


def update(troca_id, cliente=None, itens=None, data=None):
    troca = find_by_id(troca_id)
    if troca is None:
        return None
    if cliente is not None:
        troca.cliente = cliente
    if itens is not None:
        troca.item = itens
    if data is not None:
        troca.data = data
    return troca


def delete(troca_id):
    troca = find_by_id(troca_id)
    if troca is None:
        return False
    _troca_store.remove(troca)
    return True
