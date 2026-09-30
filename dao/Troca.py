import json

from sqlalchemy import text

from dao.index import Session
from model.Cliente import Cliente
from model.Item import Item
from model.Produto import Produto


def _build_cliente_payload(cliente):
    if isinstance(cliente, dict):
        return cliente
    if cliente is None:
        return None
    return {
        "id": getattr(cliente, "id", None),
        "nome": getattr(cliente, "nome", None),
        "telefone": getattr(cliente, "telefone", None),
        "email": getattr(cliente, "email", None),
        "cpf": getattr(cliente, "cpf", None),
        "endereco": getattr(cliente, "endereco", None),
    }


def _build_itens_payload(itens):
    if itens is None:
        return []
    payload = []
    for item in itens:
        if isinstance(item, dict):
            payload.append(item)
            continue
        produto = getattr(item, "produto", None)
        payload.append({
            "quantidade": getattr(item, "quantidade", 0),
            "produto": {
                "nome": getattr(produto, "nome", None),
                "preco": getattr(produto, "preco", 0),
                "descricao": getattr(produto, "descricao", None),
            },
        })
    return payload


def create(cliente, itens, data):
    with Session() as session:
        cliente_payload = _build_cliente_payload(cliente)
        itens_payload = _build_itens_payload(itens)
        cliente_id = cliente_payload.get("id") if cliente_payload else None
        result = session.execute(
            text("INSERT INTO troca (data, cliente, item) VALUES (:data, :cliente, :item)"),
            {
                "data": data,
                "cliente": str(cliente_id),
                "item": json.dumps(itens_payload),
            },
        )
        session.commit()
        troca_id = result.lastrowid
        return find_by_id(troca_id)


def list_all():
    with Session() as session:
        rows = session.execute(
            text("SELECT id, data, cliente, item FROM troca ORDER BY id")
        ).fetchall()
        dados = []
        for row in rows:
            cliente_payload = {"id": int(row.cliente)} if row.cliente not in (None, "") else None
            itens_payload = json.loads(row.item or "[]")
            dados.append({
                "id": row.id,
                "data": row.data,
                "cliente": cliente_payload,
                "itens": itens_payload,
            })
        return dados


def find_by_id(troca_id):
    with Session() as session:
        row = session.execute(
            text("SELECT id, data, cliente, item FROM troca WHERE id = :id"),
            {"id": troca_id},
        ).fetchone()
        if row is None:
            return None
        cliente_payload = {"id": int(row.cliente)} if row.cliente not in (None, "") else None
        itens_payload = json.loads(row.item or "[]")
        return {
            "id": row.id,
            "data": row.data,
            "cliente": cliente_payload,
            "itens": itens_payload,
        }


def update(troca_id, cliente=None, itens=None, data=None):
    with Session() as session:
        row = session.execute(
            text("SELECT id, data, cliente, item FROM troca WHERE id = :id"),
            {"id": troca_id},
        ).fetchone()
        if row is None:
            return None

        novo_data = data or row.data
        novo_cliente = cliente
        novo_itens = itens
        if cliente is not None:
            novo_cliente = _build_cliente_payload(cliente)
        if itens is not None:
            novo_itens = _build_itens_payload(itens)

        cliente_id = novo_cliente.get("id") if isinstance(novo_cliente, dict) else None
        session.execute(
            text("UPDATE troca SET data = :data, cliente = :cliente, item = :item WHERE id = :id"),
            {
                "data": novo_data,
                "cliente": str(cliente_id) if cliente_id is not None else row.cliente,
                "item": json.dumps(novo_itens if novo_itens is not None else json.loads(row.item or "[]")),
                "id": troca_id,
            },
        )
        session.commit()
        return find_by_id(troca_id)


def delete(troca_id):
    with Session() as session:
        result = session.execute(
            text("DELETE FROM troca WHERE id = :id"),
            {"id": troca_id},
        )
        session.commit()
        return result.rowcount > 0
