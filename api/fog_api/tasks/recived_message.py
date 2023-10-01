

from fog_api.tasks.new_device import adicionar_dispositivo
from fog_api.tasks.change_status import check_return

def message_recived(message):

    if message.get("ativar_owner"):
        adicionar_dispositivo(message)
    elif message.get("atualizado"):
        check_return(message)
