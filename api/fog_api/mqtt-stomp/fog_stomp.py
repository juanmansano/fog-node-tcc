import time
import sys
import json

import stomp
import mariadb

sub_topic = "/queue/end_point"    # receive messages on this topic

pub_topic = "/queue/fog"       # send messages to this topic

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('received an error "%s"' % frame.body)
         
    def on_message(self, frame):
        start = time.time()
        print(sys.getsizeof(frame))
        message = str(frame.body)
        print('received a message "%s"' % frame.body)
        mensagem_json = json.loads(message)
        print(mensagem_json)
        if(mensagem_json.get('login')):
           testar_login(mensagem_json, start)
        elif(mensagem_json.get('new_login')):
           adicionar_login(mensagem_json, start)
        else:
            resolve_atividade(mensagem_json.get('atividade'), start)
            

def testar_login(mensagem, start):
    db = mariadb.connect(user = "juan",
                         host="localhost",
                         password="juan",
                         database="tcc",
                         autocommit=True)

    cursor = db.cursor()

    usuario = mensagem['login']
    senha = mensagem['senha']
    email = mensagem['email']

    cursor.execute("""SELECT * FROM tcc.login where
                        (usuario = '{}' or email = '{}')
                    """.format(usuario, email))
    if(len(cursor.fetchall()) > 0):
        cursor.execute("""SELECT * FROM tcc.login where
                        usuario = '{}' and senha = '{}'
                    """.format(usuario, senha))
        if(len(cursor.fetchall()) > 0):
            print('usuario logado com sucesso')
            log_msg = {'logado': 1}
        else:
            print('usuario ou senha incorreta')
            log_msg = {'logado': 0}
    else:
        print('usuario inexistente')
        log_msg = {'logado': 2}

    cursor.close()
    db.close()
    
    conn.send(body=str(log_msg), destination=pub_topic)
    end = time.time()
    print(end-start)
    
    
def adicionar_login(mensagem, start):
    db = mariadb.connect(user = "juan",
                         host="localhost",
                         password="juan",
                         database="tcc",
                         autocommit=True)

    cursor = db.cursor()

    usuario = mensagem['new_login']
    senha = mensagem['new_senha']
    email = mensagem['new_email']

    cursor.execute("""SELECT * FROM tcc.login where
                        (usuario = '{}' or email = '{}')
                    """.format(usuario, email))
    if(len(cursor.fetchall()) > 0):
        print('usuario já existe!')
        log_msg = {'new_logado': 0}
    else:
        cursor.execute("""INSERT INTO login(usuario, senha, email)
                            VALUES('{}', '{}', '{}')
                        """.format(usuario, senha, email))
        print('usuario adicionado com sucesso')
        log_msg = {'new_logado': 1}

    cursor.close()
    db.close()
    
    conn.send(body=str(log_msg), destination=pub_topic)
    
    end = time.time()
    print(end-start)
        
        
def resolve_atividade(atividade, start):
    if(atividade == 1):
        sensor_data = {'luminosidade': 10}
    elif(atividade == 2):
        sensor_data = {'luminosidade': 50}
    elif(atividade == 3):
        sensor_data = {'luminosidade': 100}
    elif(atividade == 4):
        sensor_data = {'luminosidade': 150}
    elif(atividade == 5):
        sensor_data = {'luminosidade': 200}
    else:
        sensor_data = {'luminosidade': 0}
    print(str(sensor_data))
    conn.send(body=str(sensor_data), destination=pub_topic)
    end = time.time()
    print(end-start)
    
conn = stomp.Connection()
conn.set_listener('', MyListener())
conn.connect('juan', 'juan1234', wait=True)

conn.subscribe(destination=sub_topic, id=1, ack='auto')

