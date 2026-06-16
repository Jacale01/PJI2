from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from model.Produto import Produto
from model.Cliente import Cliente
from model.Item import Item
from dao.Traducao import create as dao_create_traducao, list_all as dao_list_traducoes, find_by_id as dao_find_traducao, update as dao_update_traducao, delete as dao_delete_traducao
from dao.Troca import create as dao_create_troca, list_all as dao_list_trocas, find_by_id as dao_find_troca, update as dao_update_troca, delete as dao_delete_troca

traducao_bp = Blueprint("traducao_bp", __name__)
troca_bp = Blueprint("troca_bp", __name__)


example_cliente_1 = Cliente(
    nome="Maria Santos",
    telefone="11999999999",
    email="maria@example.com",
    id=1,
    cpf="12345678900",
    endereco="Rua A, 100",
)
example_produto_1 = Produto(
    nome="Painel Solar",
    preco=1500.0,
    descricao="Painel solar 400W",
)
example_item_1 = Item(quantidade=2, produto=example_produto_1)

example_cliente_2 = Cliente(
    nome="João Silva",
    telefone="11988887777",
    email="joao@example.com",
    id=2,
    cpf="98765432100",
    endereco="Rua B, 200",
)
example_produto_2 = Produto(
    nome="Inversor Solar",
    preco=2500.0,
    descricao="Inversor 5kW",
)
example_item_2 = Item(quantidade=1, produto=example_produto_2)

example_traducoes = [
    dao_create_traducao(120.0),
    dao_create_traducao(45.0),
]
example_trocas = [
    dao_create_troca(cliente=example_cliente_1, itens=[example_item_1], data=datetime.now().strftime("%Y-%m-%d")),
    dao_create_troca(cliente=example_cliente_2, itens=[example_item_2], data=datetime.now().strftime("%Y-%m-%d")),
]


def build_cliente(data):
    if not isinstance(data, dict):
        abort(400, description="cliente deve ser um objeto JSON")
    required = ["nome", "telefone", "email", "id", "cpf", "endereco"]
    for field in required:
        if field not in data:
            abort(400, description=f"campo '{field}' é obrigatório em cliente")
    return Cliente(
        nome=data["nome"],
        telefone=data["telefone"],
        email=data["email"],
        id=data["id"],
        cpf=data["cpf"],
        endereco=data["endereco"],
    )


def build_produto(data):
    if not isinstance(data, dict):
        abort(400, description="produto deve ser um objeto JSON")
    for field in ["nome", "preco", "descricao"]:
        if field not in data:
            abort(400, description=f"campo '{field}' é obrigatório em produto")
    return Produto(
        nome=data["nome"],
        preco=float(data["preco"]),
        descricao=data["descricao"],
    )


def build_item(data):
    if not isinstance(data, dict):
        abort(400, description="item deve ser um objeto JSON")
    if "quantidade" not in data or "produto" not in data:
        abort(400, description="item deve conter 'quantidade' e 'produto'")
    produto = build_produto(data["produto"])
    quantidade = int(data["quantidade"])
    return Item(quantidade=quantidade, produto=produto)


def traducao_to_dict(traducao):
    return {
        "id": traducao.getId(),
        "energiaGerada": traducao.getEnergiaGerada(),
        "tokensGerados": traducao.calcularTokensGerados(),
    }


def troca_to_dict(troca):
    return {
        "id": troca.getId(),
        "data": troca.getData(),
        "cliente": {
            "id": troca.getCliente().getId(),
            "nome": troca.getCliente().getNome(),
            "telefone": troca.getCliente().getTelefone(),
            "email": troca.getCliente().getEmail(),
            "cpf": troca.getCliente().getCpf(),
            "endereco": troca.getCliente().getEndereco(),
        },
        "itens": [
            {
                "quantidade": item.getQuantidade(),
                "produto": {
                    "nome": item.getProduto().getNome(),
                    "descricao": item.getProduto().getDescricao(),
                    "preco": item.getProduto().getPreco(),
                },
                "subValor": item.getSubValor(),
            }
            for item in troca.getItem()
        ],
        "valorTotal": troca.getValorTotal(),
    }


@traducao_bp.route("/traducao", methods=["POST"])
def criar_traducao():
    data = request.get_json(force=True)
    if data is None or "energiaGerada" not in data:
        abort(400, description="campo 'energiaGerada' é obrigatório")

    energia = float(data["energiaGerada"])
    traducao = dao_create_traducao(energia)
    return jsonify(traducao_to_dict(traducao)), 201


@traducao_bp.route("/traducao", methods=["GET"])
def listar_traducoes():
    return jsonify([traducao_to_dict(t) for t in dao_list_traducoes()]), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["GET"])
def obter_traducao(traducao_id):
    traducao = dao_find_traducao(traducao_id)
    if traducao is None:
        abort(404, description="Tradução não encontrada")
    return jsonify(traducao_to_dict(traducao)), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["PUT"])
def atualizar_traducao(traducao_id):
    data = request.get_json(force=True)
    if data is None or "energiaGerada" not in data:
        abort(400, description="campo 'energiaGerada' é obrigatório")

    traducao = dao_update_traducao(traducao_id, float(data["energiaGerada"]))
    if traducao is None:
        abort(404, description="Tradução não encontrada")
    return jsonify(traducao_to_dict(traducao)), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["DELETE"])
def deletar_traducao(traducao_id):
    deleted = dao_delete_traducao(traducao_id)
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

    troca = dao_create_troca(cliente=cliente, itens=itens, data=data_troca)
    return jsonify(troca_to_dict(troca)), 201


@troca_bp.route("/troca", methods=["GET"])
def listar_trocas():
    return jsonify([troca_to_dict(t) for t in dao_list_trocas()]), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["GET"])
def obter_troca(troca_id):
    troca = dao_find_troca(troca_id)
    if troca is None:
        abort(404, description="Troca não encontrada")
    return jsonify(troca_to_dict(troca)), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["PUT"])
def atualizar_troca(troca_id):
    data = request.get_json(force=True)
    if data is None:
        abort(400, description="JSON inválido")

    cliente = build_cliente(data["cliente"]) if "cliente" in data else None
    itens = [build_item(item_data) for item_data in data["itens"]] if "itens" in data else None
    data_troca = data.get("data") if "data" in data else None

    troca = dao_update_troca(troca_id, cliente=cliente, itens=itens, data=data_troca)
    if troca is None:
        abort(404, description="Troca não encontrada")
    return jsonify(troca_to_dict(troca)), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["DELETE"])
def deletar_troca(troca_id):
    deleted = dao_delete_troca(troca_id)
    if not deleted:
        abort(404, description="Troca não encontrada")
    return jsonify({"mensagem": "Troca removida com sucesso"}), 200
