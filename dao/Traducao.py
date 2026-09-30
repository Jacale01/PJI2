import json

from sqlalchemy import text

from dao.index import Session
from model.Traducao import Traducao


def create(energia_gerada):
    with Session() as session:
        result = session.execute(
            text("INSERT INTO traducao (energiaGerada) VALUES (:energiaGerada)"),
            {"energiaGerada": float(energia_gerada)},
        )
        session.commit()
        traducao_id = result.lastrowid
        return find_by_id(traducao_id)


def list_all():
    with Session() as session:
        rows = session.execute(
            text("SELECT id, energiaGerada FROM traducao ORDER BY id")
        ).fetchall()
        return [
            {"id": row.id, "energiaGerada": float(row.energiaGerada)}
            for row in rows
        ]


def find_by_id(traducao_id):
    with Session() as session:
        row = session.execute(
            text("SELECT id, energiaGerada FROM traducao WHERE id = :id"),
            {"id": traducao_id},
        ).fetchone()
        if row is None:
            return None
        return {
            "id": row.id,
            "energiaGerada": float(row.energiaGerada),
        }


def update(traducao_id, energia_gerada):
    with Session() as session:
        result = session.execute(
            text("UPDATE traducao SET energiaGerada = :energiaGerada WHERE id = :id"),
            {"energiaGerada": float(energia_gerada), "id": traducao_id},
        )
        session.commit()
        if result.rowcount == 0:
            return None
        return find_by_id(traducao_id)


def delete(traducao_id):
    with Session() as session:
        result = session.execute(
            text("DELETE FROM traducao WHERE id = :id"),
            {"id": traducao_id},
        )
        session.commit()
        return result.rowcount > 0
