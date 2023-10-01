

from fog_api.tasks.new_device import adicionar_dispositivo
from fog_api.tasks.change_status import check_return


def message_recived(dispositivo_id, atividade_id, message):

    if message["ativar_owner"]:
        adicionar_dispositivo(message)
    elif message["atualizado"]:
        check_return(message)
