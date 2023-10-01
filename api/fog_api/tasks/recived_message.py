

from fog_api.tasks.new_device import adicionar_dispositivo
from fog_api.tasks.change_status import check_return

import json

def message_recived(message):
    print("function message recived")
    print(message)
    if message.get("ativar_owner"):
        adicionar_dispositivo(message)
    elif message["atualizado"]:
        check_return(message)
