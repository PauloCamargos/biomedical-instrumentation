import paho.mqtt.client as mqtt
import time

"""
SHORT EXAMPLE FOR MQTT COMMUNICATION.

To install Mqtt client and broker, follow the instructions 
in the README.md file, inside the '.py' folder.

Before you run the program, make sure you've started the
Mosquitto broker in your terminal/cmd by running:

$ mosquitto -v

It should be running on port 1883 by default.
"""

# CALLBACK METHOD
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
    # Show the received message
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("[OK] MENSAGEM RECEBIDA: ", m_decode)


def publish_message(topic, movement):
    # PUBLISHING A VALUE IN A TOPIC
    client.publish(topic, movement)


# BROKER ADDRESS
broker = "127.0.0.1"
# CREATING A NEW CLIENT
client = mqtt.Client("python1")

# SETTING THE CALLBACK FUNCTIONS TO THE CREATED 'client'
client.on_connect=on_connect
client.on_disconnect=on_disconnet
client.on_log=on_log
client.on_message=on_message

# DEBUG
print("[OK] Conectando ao broker ", broker)

# Conneting to broker (mosquitto)
client.connect(broker,port=1883)
client.loop_start()

# Subscribing to the topic 'move'
# It means that everything published in this topic will be received 
# by the 'client'
topic = 'move'
client.subscribe(topic)

# Array conaining messages to be sent 
moves = ['down', 'up', 'left', 'right', 's', 'p']

for m in moves:
    publish_message(topic, m)
    print(f"[INFO] Executando o movimento {m}")
    time.sleep(3)

# Closing connection
client.loop_stop()
client.disconnect()