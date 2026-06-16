from model.Traducao import Traducao

_traducao_store = []
_next_traducao_id = 1


def create(energiaGerada):
    global _next_traducao_id
    traducao = Traducao(energiaGerada=energiaGerada, id=_next_traducao_id)
    _traducao_store.append(traducao)
    _next_traducao_id += 1
    return traducao


def list_all():
    return list(_traducao_store)


def find_by_id(traducao_id):
    return next((t for t in _traducao_store if t.getId() == traducao_id), None)


def update(traducao_id, energiaGerada):
    traducao = find_by_id(traducao_id)
    if traducao is None:
        return None
    traducao.energiaGerada = energiaGerada
    return traducao


def delete(traducao_id):
    traducao = find_by_id(traducao_id)
    if traducao is None:
        return False
    _traducao_store.remove(traducao)
    return True
