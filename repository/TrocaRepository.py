from dao.Troca import create, list_all, find_by_id, update, delete


class TrocaRepository:
    @staticmethod
    def create(cliente, itens, data):
        return create(cliente, itens, data)

    @staticmethod
    def list_all():
        return list_all()

    @staticmethod
    def find_by_id(troca_id):
        return find_by_id(troca_id)

    @staticmethod
    def update(troca_id, cliente=None, itens=None, data=None):
        return update(troca_id, cliente=cliente, itens=itens, data=data)

    @staticmethod
    def delete(troca_id):
        return delete(troca_id)
