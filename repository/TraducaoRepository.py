from dao.Traducao import create, list_all, find_by_id, update, delete


class TraducaoRepository:
    @staticmethod
    def create(energia_gerada):
        return create(energia_gerada)

    @staticmethod
    def list_all():
        return list_all()

    @staticmethod
    def find_by_id(traducao_id):
        return find_by_id(traducao_id)

    @staticmethod
    def update(traducao_id, energia_gerada):
        return update(traducao_id, energia_gerada)

    @staticmethod
    def delete(traducao_id):
        return delete(traducao_id)
