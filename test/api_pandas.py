# import pandas as pd
# import numpy as np
import requests
import json
# from datetime import datetime
# import time
# import random

url = "http://192.168.1.22:5210/novaAutorizacao"

# payload = "{new_login: 'juan', new_senha: 'juan1234', new_email: 'juan@gmail.com'}"
# payload = "{login: 'juan', senha: 'juan1234', email: 'juan@gmail.com'}"
payload = '{"email": "joao@gmail.com", "id_dispositivo": 1, "ativo": 1}'
# payload = "{usuario: 1}"
# payload = "{lista_atividade: 1}"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOJIUzI1NiJ9.eyJub21lIjoiSnVhbiIsImVtYWlsIjoianVhbkBnbWFpbC5jb20iLCJleHAiOjE2NjkxNTUwOTB9.BfQXeVtnEh3Sf88tN6oF5ST5g5h3ZQWn9jTK59kWS3s'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response)

_jsons = json.loads(response.content)

print(_jsons)


# inicio = datetime.now()
# payload = "{atividade: 0}"
# headers = {
#     'Content-Type': 'application/json'
# }
# response = requests.request("POST", url, headers=headers, data=payload)
# # print(response.text)
# final = datetime.now()
# data = np.array([[inicio, final, final - inicio]])
# df = pd.DataFrame(data, columns=['inicio','final','diferenca'])
# time.sleep(10)

# for i in range(1,30,1):
#     print(i)
#     id = random.randint(0,5)
#     inicio = datetime.now()
#     payload = "atividade: {}".format(id)
#     payload = '{' + payload + '}'
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     final = datetime.now()
#     data = np.array([inicio, final, final - inicio])
#     df.loc[i] = data
#     time.sleep(10)

# print(df["diferenca"])