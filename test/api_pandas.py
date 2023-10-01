import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import time
import random

url = "http://tccmansano.ddns.net:5210/dispositivos/usuario=1"

# payload = "{new_login: 'juan', new_senha: 'juan1234', new_email: 'juan@gmail.com'}"
# payload = "{login: 'juan', senha: 'juan1234', email: 'juan@gmail.com'}"
# payload = '{"email": "joao@gmail.com", "id_dispositivo": 1, "ativo": 0}'
# payload = "{usuario: 1}"
# payload = "{lista_atividade: 1}"
# headers = {
    # 'Content-Type': 'application/json',
    # 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOJIUzI1NiJ9.eyJub21lIjoiSnVhbiIsImVtYWlsIjoianVhbkBnbWFpbC5jb20iLCJleHAiOjE2NjkxNTUwOTB9.BfQXeVtnEh3Sf88tN6oF5ST5g5h3ZQWn9jTK59kWS3s'
# }

inicio = datetime.now()
print(inicio)
id = 1
payload = {"usuario_ultima_atualizacao": 1, "id_ultima_atividade": id}
payload = json.dumps(payload)
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibm9tZSI6Ikp1YW4iLCJlbWFpbCI6Imp1YW5tYW5zYW5vQGdtYWlsLmNvbSIsImV4cCI6MTY5ODI3NTkzNH0.CbwCzySfkBFOrMnRKs5AqT7I9p7Cvkv8hKEvBcR_UUU'
}
response = requests.request("POST", url, headers=headers, data=payload)
final = datetime.now()
print(final)
data = np.array([[inicio, final, final - inicio]])
df = pd.DataFrame(data, columns=['inicio','final','diferenca'])
# time.sleep(10)

# for i in range(1,30,1):
#     print(i)
#     diff = False
#     while not diff:
#         new_id = random.randint(1,5)
#         if id != new_id:
#             id = new_id
#             diff = True
#     inicio = datetime.now()
#     print(inicio)
#     payload = {"usuario_ultima_atualizacao": 1, "id_ultima_atividade": id}
#     payload = json.dumps(payload)
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibm9tZSI6Ikp1YW4iLCJlbWFpbCI6Imp1YW5tYW5zYW5vQGdtYWlsLmNvbSIsImV4cCI6MTY5ODI3NTkzNH0.CbwCzySfkBFOrMnRKs5AqT7I9p7Cvkv8hKEvBcR_UUU'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     final = datetime.now()
#     print(final)
#     data = np.array([inicio, final, final - inicio])
#     df.loc[i] = data
#     time.sleep(10)

# print(df["diferenca"])