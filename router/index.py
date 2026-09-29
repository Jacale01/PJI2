from datetime import datetime

from flask import Blueprint, abort, jsonify, request

from model.Cliente import Cliente
from model.Item import Item
from model.Produto import Produto
from services.traducao_service import (
    create_traducao as service_create_traducao,
    delete_traducao as service_delete_traducao,
    get_traducao as service_get_traducao,
    list_traducoes as service_list_traducoes,
    update_traducao as service_update_traducao,
)
from services.troca_service import (
    create_troca as service_create_troca,
    delete_troca as service_delete_troca,
    get_troca as service_get_troca,
    list_trocas as service_list_trocas,
    update_troca as service_update_troca,
)

traducao_bp = Blueprint("traducao_bp", __name__)
troca_bp = Blueprint("troca_bp", __name__)


def traducao_to_dict(traducao):
    if traducao is None:
        return None
    if isinstance(traducao, dict):
        return {
            "id": traducao.get("id"),
            "energiaGerada": traducao.get("energiaGerada"),
        }
    return {
        "id": getattr(traducao, "id", None),
        "energiaGerada": getattr(traducao, "energiaGerada", None),
        "tokensGerados": getattr(traducao, "tokensGerados", None),
    }


def build_cliente(data):
    if data is None:
        return None
    return Cliente(
        nome=data.get("nome", ""),
        telefone=data.get("telefone", ""),
        email=data.get("email", ""),
        id=data.get("id"),
        cpf=data.get("cpf", ""),
        endereco=data.get("endereco", ""),
    )


def build_item(item_data):
    produto_data = item_data.get("produto", {})
    produto = Produto(
        nome=produto_data.get("nome", ""),
        preco=float(produto_data.get("preco", 0)),
        descricao=produto_data.get("descricao", ""),
    )
    return Item(
        quantidade=int(item_data.get("quantidade", 0)),
        produto=produto,
    )


def troca_to_dict(troca):
    if troca is None:
        return None
    if isinstance(troca, dict):
        return {
            "id": troca.get("id"),
            "data": troca.get("data"),
            "cliente": troca.get("cliente"),
            "itens": troca.get("itens", []),
        }
    return {
        "id": getattr(troca, "id", None),
        "data": getattr(troca, "data", None),
        "cliente": getattr(troca, "cliente", None),
        "itens": getattr(troca, "itens", []),
    }


@traducao_bp.route("/traducao", methods=["POST"])
def criar_traducao():
    data = request.get_json(force=True)
    if data is None or "energiaGerada" not in data:
        abort(400, description="campo 'energiaGerada' é obrigatório")

    try:
        traducao = service_create_traducao(data["energiaGerada"])
    except ValueError as exc:
        abort(400, description=str(exc))
    return jsonify(traducao_to_dict(traducao)), 201


@traducao_bp.route("/traducao", methods=["GET"])
def listar_traducoes():
    return jsonify([traducao_to_dict(t) for t in service_list_traducoes()]), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["GET"])
def obter_traducao(traducao_id):
    traducao = service_get_traducao(traducao_id)
    if traducao is None:
        abort(404, description="Tradução não encontrada")
    return jsonify(traducao_to_dict(traducao)), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["PUT"])
def atualizar_traducao(traducao_id):
    data = request.get_json(force=True)
    if data is None or "energiaGerada" not in data:
        abort(400, description="campo 'energiaGerada' é obrigatório")

    try:
        traducao = service_update_traducao(traducao_id, data["energiaGerada"])
    except ValueError as exc:
        abort(400, description=str(exc))
    if traducao is None:
        abort(404, description="Tradução não encontrada")
    return jsonify(traducao_to_dict(traducao)), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["DELETE"])
def deletar_traducao(traducao_id):
    deleted = service_delete_traducao(traducao_id)
    if not deleted:
        abort(404, description="Tradução não encontrada")
    return jsonify({"mensagem": "Tradução removida com sucesso"}), 200


@troca_bp.route("/troca", methods=["POST"])
def criar_troca():
    data = request.get_json(force=True)
    if data is None:
        abort(400, description="JSON inválido")
    if "cliente" not in data or "itens" not in data:
        abort(400, description="campos 'cliente' e 'itens' são obrigatórios")

    cliente = build_cliente(data["cliente"])
    itens = [build_item(item_data) for item_data in data["itens"]]
    data_troca = data.get("data", datetime.now().strftime("%Y-%m-%d"))

    try:
        troca = service_create_troca(cliente=data["cliente"], itens=data["itens"], data=data_troca)
    except ValueError as exc:
        abort(400, description=str(exc))
    return jsonify(troca_to_dict(troca)), 201


@troca_bp.route("/troca", methods=["GET"])
def listar_trocas():
    return jsonify([troca_to_dict(t) for t in service_list_trocas()]), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["GET"])
def obter_troca(troca_id):
    troca = service_get_troca(troca_id)
    if troca is None:
        abort(404, description="Troca não encontrada")
    return jsonify(troca_to_dict(troca)), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["PUT"])
def atualizar_troca(troca_id):
    data = request.get_json(force=True)
    if data is None:
        abort(400, description="JSON inválido")

    cliente = data.get("cliente")
    itens = data.get("itens")
    data_troca = data.get("data")

    troca = service_update_troca(troca_id, cliente=cliente, itens=itens, data=data_troca)
    if troca is None:
        abort(404, description="Troca não encontrada")
    return jsonify(troca_to_dict(troca)), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["DELETE"])
def deletar_troca(troca_id):
    deleted = service_delete_troca(troca_id)
    if not deleted:
        abort(404, description="Troca não encontrada")
    return jsonify({"mensagem": "Troca removida com sucesso"}), 200

