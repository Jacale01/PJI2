from repository.TraducaoRepository import TraducaoRepository


def create_traducao(energia_gerada):
    if energia_gerada is None:
        raise ValueError("campo 'energiaGerada' é obrigatório")
    return TraducaoRepository.create(float(energia_gerada))


def list_traducoes():
    return TraducaoRepository.list_all()


def get_traducao(traducao_id):
    return TraducaoRepository.find_by_id(traducao_id)


def update_traducao(traducao_id, energia_gerada):
    if energia_gerada is None:
        raise ValueError("campo 'energiaGerada' é obrigatório")
    return TraducaoRepository.update(traducao_id, float(energia_gerada))


def delete_traducao(traducao_id):
    return TraducaoRepository.delete(traducao_id)
