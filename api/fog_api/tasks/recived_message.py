

from fog_api.tasks.new_device import adicionar_dispositivo
import fog_api.tasks.change_status as cs
def message_recived(message):
    print(message)
    if message.get("ativar_owner"):
        adicionar_dispositivo(message)
    elif message.get("atualizado"):
        cs.answer = message
