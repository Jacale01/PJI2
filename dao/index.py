import json

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///meu_banco.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def criar_tabela(session):
    tabelas = (
        """CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS produto (
            nome TEXT PRIMARY KEY,
            preco REAL NOT NULL,
            descricao TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quantidade INTEGER NOT NULL,
            produto TEXT NOT NULL,
            FOREIGN KEY(produto) REFERENCES produto(nome)
        )""",
        """CREATE TABLE IF NOT EXISTS energiaGerada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quantidade INTEGER NOT NULL,
            periodo TEXT NOT NULL,
            cliente INTEGER NOT NULL,
            FOREIGN KEY(cliente) REFERENCES cliente(id)
        )""",
        """CREATE TABLE IF NOT EXISTS token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataExpedicao TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS carteira (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            senha TEXT NOT NULL,
            cliente INTEGER NOT NULL,
            tokens TEXT NOT NULL,
            FOREIGN KEY(cliente) REFERENCES cliente(id)
        )""",
        """CREATE TABLE IF NOT EXISTS troca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            cliente TEXT NOT NULL,
            item TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS traducao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            energiaGerada REAL NOT NULL
        )""",
    )
    for sql in tabelas:
        session.execute(text(sql))
    session.commit()


def _valor_id(valor):
    return getattr(valor, "id", valor)


def _valor_nome(valor):
    return getattr(valor, "nome", valor)


def _inserir(session, sql, parametros):
    resultado = session.execute(text(sql), parametros)
    session.commit()
    return resultado.rowcount


def inserirCliente(session, nome, telefone, email, cpf, endereco):
    return _inserir(
        session,
        """INSERT INTO cliente (nome, telefone, email, cpf, endereco)
           VALUES (:nome, :telefone, :email, :cpf, :endereco)""",
        {"nome": nome, "telefone": telefone, "email": email, "cpf": cpf, "endereco": endereco},
    )


def inserirProduto(session, nome, preco, descricao):
    return _inserir(
        session,
        "INSERT INTO produto (nome, preco, descricao) VALUES (:nome, :preco, :descricao)",
        {"nome": nome, "preco": preco, "descricao": descricao},
    )


def inserirItem(session, quantidade, produto):
    return _inserir(
        session,
        "INSERT INTO item (quantidade, produto) VALUES (:quantidade, :produto)",
        {"quantidade": quantidade, "produto": _valor_nome(produto)},
    )


def inserirEnergiaGerada(session, quantidade, periodo, cliente):
    return _inserir(
        session,
        """INSERT INTO energiaGerada (quantidade, periodo, cliente)
           VALUES (:quantidade, :periodo, :cliente)""",
        {"quantidade": quantidade, "periodo": periodo, "cliente": _valor_id(cliente)},
    )


def inserirToken(session, dataExpedicao, id=None):
    if id is None:
        return _inserir(
            session,
            "INSERT INTO token (dataExpedicao) VALUES (:dataExpedicao)",
            {"dataExpedicao": dataExpedicao},
        )
    return _inserir(
        session,
        "INSERT INTO token (id, dataExpedicao) VALUES (:id, :dataExpedicao)",
        {"id": id, "dataExpedicao": dataExpedicao},
    )


def inserirCarteira(session, senha, cliente, tokens, codigo=None):
    parametros = {
        "senha": senha,
        "cliente": _valor_id(cliente),
        "tokens": json.dumps(tokens, default=lambda token: getattr(token, "id", token)),
    }
    if codigo is None:
        return _inserir(
            session,
            "INSERT INTO carteira (senha, cliente, tokens) VALUES (:senha, :cliente, :tokens)",
            parametros,
        )
    parametros["codigo"] = codigo
    return _inserir(
        session,
        """INSERT INTO carteira (codigo, senha, cliente, tokens)
           VALUES (:codigo, :senha, :cliente, :tokens)""",
        parametros,
    )


def inserirTroca(session, data, cliente, item):
    return _inserir(
        session,
        "INSERT INTO troca (data, cliente, item) VALUES (:data, :cliente, :item)",
        {
            "data": data,
            "cliente": str(_valor_id(cliente)),
            "item": json.dumps(item, default=lambda valor: getattr(valor, "nome", valor)),
        },
    )


def inserirTraducao(session, energiaGerada):
    return _inserir(
        session,
        "INSERT INTO traducao (energiaGerada) VALUES (:energiaGerada)",
        {"energiaGerada": energiaGerada},
    )


with Session() as session:
    criar_tabela(session)


