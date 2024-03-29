import time
import json
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import mariadb
import collections


Broker = "tccmansano.ddns.net"

sub_topic = "end_point"    # receive messages on this topic

pub_topic = "fog"       # send messages to this topic

QOS = 0 #qos para sub e pub

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic, QOS)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    if(msg.retain == 1):
        pass
    else:
        start = time.time()
        message = str(msg.payload)
        print(message)
        list = message.split("'")
        if(not message.startswith("b'test")):
            mensagem_json = json.loads(list[1])
            print(mensagem_json)
            if(mensagem_json.get('ativar')):
                adicionar_dispositivo(mensagem_json)    
    
       
def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))
    

client = mqtt.Client("fog_")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("juan", "juan1234")
client.connect(Broker, 1883)
client.loop_start()