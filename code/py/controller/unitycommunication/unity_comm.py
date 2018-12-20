# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 17:55:58 2018

@author: paulo
"""
import os
import subprocess
import paho.mqtt.client as mqtt
import time

def open_mosquitto_broker():
    """
    Opens a Mosquitto broker
    """
    
    print('[INFO] Opening Mosquitto broker...')
    os.popen('mosquitto')
    # subprocess.call(['C:\Program Files\mosquitto\mosquitto.exe'])
    print('[OK] Success! Sever running.')
    

# CALLBACK METHODs
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


def publish_message(client, topic, message):
    # PUBLISHING A VALUE IN A TOPIC
    client.publish(topic, message)


def relay_movement_command(movement_index=1):
    open_mosquitto_broker()
    movements = {1:'abre', 2:'fecha', 3:'flexao', 4:'extensao', 5:'supinacao', 6:'pronacao'}

    # BROKER ADDRESS
    broker = "127.0.0.1"
    # CREATING A NEW CLIENT
    client = mqtt.Client("python1")
    
    # SETTING THE CALLBACK FUNCTIONS TO THE CREATED 'client'
    client.on_connect=on_connect
    client.on_disconnect=on_disconnet
    client.on_log=on_log
#    client.on_message=on_message
    
    # DEBUG
    print("[OK] Conectando ao broker ", broker)
    
    # Subscribing to the topic 'move'
    # It means that everything published in this topic will be received 
    # by the 'client'
    topic = 'move'
    client.subscribe(topic)
    # Conneting to broker (mosquitto)
    client.connect(broker,port=1883)
    client.loop_start()
    print(f"[OK] Received movement: {movement_index} - {movements.get(movement_index)}")
    client.publish(topic, movements.get(movement_index))
    print(f"[OK] Relayed command: {movement_index} - {movements.get(movement_index)}")
    # Closing connection
    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    pass    
