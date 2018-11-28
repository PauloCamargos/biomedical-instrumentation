import numpy
import matplotlib
import serial 
import sklearn
import pandas
import paho.mqtt.client as mqtt
import time

# MÉTODOS DE CALLBACK
def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("[OK] Connection made")
    else:
        print("[ERROR] Connection NOT made. Code:  ", rc )


def on_disconnet(client, userdata, flags, rc=0):
    print("[OK] Disconnected. Code: ", rc)


def on_message(client,userdata, msg):
    # Exibe a mensagem recebida
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("[RECEBIDA] MENSAGEM RECEBIDA: \n", m_decode)

# ENDERECO DO BROKER
broker = "127.0.0.1"
# Criando um novo cliente
client = mqtt.Client("python1")

# Configurando as funções de callback no objeto criado 'client' 
client.on_connect=on_connect
client.on_disconnect=on_disconnet
client.on_log=on_log
client.on_message=on_message

def execute_movement(topic, movement):
    # Publicando um valor neste topico
    client.publish(topic, movement)

# DEBUG
print("Conectando ao broker ", broker)

# Conectando ao broker (mosquitto)
client.connect(broker,port=1883)
client.loop_start()

# Subscrevendo a um novo topico
topic = 'move'
client.subscribe(topic)


# Array de comandos
moves = ['down', 'up', 'left', 'right', 's', 'p']

for m in moves:
    execute_movement(topic, m)
    print(f"Executando o movimento {m}")
    time.sleep(5)

# Fechando a conexãa
client.loop_stop()
client.disconnect()